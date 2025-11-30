"""Command executor plugin implementation."""

import subprocess
import shlex
from kai.plugins.base import Plugin
from kai.core.intent import Intent


class CommandExecutorPlugin(Plugin):
    """Plugin for executing Linux commands."""
    
    def __init__(self):
        super().__init__(
            name="command_executor",
            version="1.0.0",
            intents=["execute_command", "install_package"]
        )
        
    def _extract_package_fallback(self, text: str) -> str:
        """Fallback package name extraction.
        
        Args:
            text: User input text
            
        Returns:
            Package name or None
        """
        text_lower = text.lower()
        
        # Try to extract after "install"
        words = text_lower.split()
        for i, word in enumerate(words):
            if word == 'install' and i + 1 < len(words):
                return words[i + 1]
        
        return None
    
    async def handle_intent(self, intent: Intent) -> str:
        """Handle command execution intents.
        
        Args:
            intent: Intent to handle
            
        Returns:
            Response text
        """
        text_lower = intent.raw_text.lower()
        
        # Check for install package commands
        if any(word in text_lower for word in ['install', 'apt install', 'apt-get install']):
            return await self._handle_install(intent.raw_text)
        
        # Check for execute command
        if any(word in text_lower for word in ['run command', 'execute', 'run this']):
            return await self._handle_execute(intent.raw_text)
        
        return "I'm not sure what command you want me to run."
    
    async def _handle_install(self, text: str) -> str:
        """Handle package installation.
        
        Args:
            text: User input text
            
        Returns:
            Response text
        """
        # Use LLM to extract package name
        from kai.ai.llm import LLMEngine
        
        try:
            llm = LLMEngine(model="llama3.2:3b")
            
            extract_prompt = f"""Extract the package/software name from this install request and convert it to the correct apt package name.

User request: "{text}"

Rules:
- Convert common names to apt package names (e.g., python -> python3, node -> nodejs, docker -> docker.io)
- If the name is already correct, keep it as is
- Return the actual apt package name that can be installed

Respond with ONLY the apt package name (one word), nothing else. If you can't determine it, respond with "unknown"."""

            package_name = llm.generate(extract_prompt, system_prompt="You are a package name extractor. Respond with only the package name.").strip().lower()
            
            if package_name == "unknown" or not package_name:
                return "I couldn't figure out which package you want to install. Can you be more specific?"
            
        except Exception as e:
            # Fallback to keyword matching
            package_name = self._extract_package_fallback(text)
            if not package_name:
                return "I couldn't figure out which package you want to install. Can you say it again?"
        
        # Confirm before installing
        # Get timeout from config
        from kai.core.config import Config
        config = Config()
        check_timeout = config.get("command_executor.check_timeout", 5)
        install_timeout = config.get("command_executor.install_timeout", 300)
        
        try:
            # Check if package exists
            check_cmd = f"apt-cache show {package_name}"
            result = subprocess.run(
                shlex.split(check_cmd),
                capture_output=True,
                text=True,
                timeout=check_timeout
            )
            
            if result.returncode != 0:
                return f"I couldn't find a package called {package_name}. Make sure the name is correct."
            
            # Install the package
            install_cmd = f"sudo apt-get install -y {package_name}"
            result = subprocess.run(
                shlex.split(install_cmd),
                capture_output=True,
                text=True,
                timeout=install_timeout
            )
            
            if result.returncode == 0:
                return f"Successfully installed {package_name}."
            else:
                return f"Failed to install {package_name}. You might need to run this manually with sudo."
                
        except subprocess.TimeoutExpired:
            return f"Installation of {package_name} is taking too long. Please check it manually."
        except Exception as e:
            return f"Error installing {package_name}: {str(e)}"
    
    async def _handle_execute(self, text: str) -> str:
        """Handle command execution.
        
        Args:
            text: User input text
            
        Returns:
            Response text
        """
        # Extract command (this is simplified - you might want better parsing)
        # Look for command after keywords
        keywords = ['run command', 'execute', 'run this']
        command = None
        
        text_lower = text.lower()
        for keyword in keywords:
            if keyword in text_lower:
                # Get everything after the keyword
                idx = text_lower.index(keyword) + len(keyword)
                command = text[idx:].strip()
                break
        
        if not command:
            return "I couldn't figure out which command you want to run."
        
        # Safety check using LLM
        from kai.ai.llm import LLMEngine
        
        try:
            llm = LLMEngine()
            safety_prompt = f"""Is this command safe to run on a Linux system?

Command: {command}

Consider:
- Does it delete files or format drives?
- Does it modify system files?
- Does it have potential for data loss?

Respond with ONLY "safe" or "dangerous", nothing else."""

            safety_check = llm.generate(safety_prompt, system_prompt="You are a command safety analyzer.").strip().lower()
            
            if "dangerous" in safety_check:
                return "I can't run that command as it might be dangerous to your system."
        except:
            # If LLM fails, be conservative
            dangerous_keywords = ['rm -rf', 'dd if=', 'mkfs', 'format', '> /dev/sd']
            if any(danger in command.lower() for danger in dangerous_keywords):
                return "I can't run that command as it might be dangerous to your system."
        
        # Get timeout from config
        from kai.core.config import Config
        config = Config()
        exec_timeout = config.get("command_executor.exec_timeout", 30)
        max_output_length = config.get("command_executor.max_output_length", 200)
        
        try:
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=exec_timeout
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    # Limit output length for voice
                    if len(output) > max_output_length:
                        return f"Command executed successfully. Output is too long to read, but it worked."
                    else:
                        return f"Command executed. Output: {output}"
                else:
                    return "Command executed successfully."
            else:
                error = result.stderr.strip()
                max_error_length = config.get("command_executor.max_error_length", 100)
                if error and len(error) < max_error_length:
                    return f"Command failed with error: {error}"
                else:
                    return "Command failed. Check the terminal for details."
                    
        except subprocess.TimeoutExpired:
            return "Command is taking too long. It might still be running in the background."
        except Exception as e:
            return f"Error executing command: {str(e)}"
