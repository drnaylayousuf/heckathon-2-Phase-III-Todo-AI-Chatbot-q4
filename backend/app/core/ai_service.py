"""
AI Service for integrating with Google Gemini API
"""
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from app.config import settings
from app.core.logging_config import get_logger
from app.models.task import Task as TaskModel
from app.models.conversation import ConversationMessage
from sqlmodel import Session, select
from datetime import datetime

logger = get_logger(__name__)

class GeminiService:
    """
    Service class to handle interactions with Google Gemini API
    """

    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.model = None

        if self.api_key and self.api_key != "your-gemini-api-key-here":
            try:
                genai.configure(api_key=self.api_key)

                # Try the configured model first
                model_name = settings.default_ai_model
                try:
                    self.model = genai.GenerativeModel(model_name)
                    logger.info(f"Gemini AI service initialized with model: {model_name}")
                except Exception as model_error:
                    logger.warning(f"Configured model '{model_name}' not available: {str(model_error)[:100]}...")

                    # Fallback to a known working model
                    fallback_models = ["gemini-1.5-flash", "gemini-1.0-pro", "gemini-pro-vision"]
                    self.model = None

                    for fallback_model in fallback_models:
                        try:
                            self.model = genai.GenerativeModel(fallback_model)
                            logger.info(f"Fallback: Gemini AI service initialized with model: {fallback_model}")
                            break
                        except Exception as fallback_error:
                            logger.warning(f"Fallback model '{fallback_model}' also failed: {str(fallback_error)[:100]}...")
                            continue

                    if self.model is None:
                        logger.error("No valid AI models available")
                        self.model = None

            except Exception as e:
                logger.error(f"Error initializing Gemini AI service: {str(e)[:100]}...")
                self.model = None
        else:
            logger.warning("Gemini API key not configured. AI features will be limited.")
            self.model = None

    def get_task_context(self, session: Session, user_id: str) -> str:
        """
        Get user's tasks to provide context to the AI
        """
        try:
            statement = select(TaskModel).where(TaskModel.user_id == user_id).order_by(TaskModel.created_at.desc()).limit(10)
            result = session.execute(statement)
            tasks = result.scalars().all()

            if not tasks:
                return "User has no tasks."

            task_list = []
            for task in tasks:
                task_info = f"- ID: {task.id}, Title: '{task.title}', Status: {task.status}, Priority: {task.priority}"
                if task.due_date:
                    task_info += f", Due: {task.due_date.strftime('%Y-%m-%d') if task.due_date else 'None'}"
                task_list.append(task_info)

            return f"User has {len(tasks)} tasks:\n" + "\n".join(task_list)
        except Exception as e:
            logger.error(f"Error getting task context: {e}")
            return "Error retrieving user's tasks."

    def generate_response(self, message: str, session: Session, user_id: str) -> str:
        """
        Generate AI response based on user message and task context
        """
        if not self.model:
            # Even if AI is not configured, try to handle task commands via the MCP tools in chat.py
            return "AI service is not configured. Please set up your Gemini API key in the .env file. However, you can still use task commands like 'Add a task to buy groceries' or 'Show my tasks'."

        try:
            # Get user's task context
            task_context = self.get_task_context(session, user_id)

            # Create prompt with context
            prompt = f"""
            You are a helpful AI assistant for a task management application. The user has the following tasks:

            {task_context}

            The user said: "{message}"

            Respond to the user's request in a helpful and concise way. If the user is asking to perform task operations (add, list, update, complete, delete),
            acknowledge their request and provide clear instructions or confirmations. If you need more specific information (like a task title for deletion), ask for it.

            If the user is asking general questions or having a casual conversation, engage appropriately. Keep your responses friendly and professional.
            """

            response = self.model.generate_content(prompt)
            return response.text if response.text else "I understood your request, but I couldn't generate a response. Please try rephrasing."

        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)[:100]}...")  # Log only part of the error to avoid API key exposure

            # Check if it's a model not found error and provide helpful guidance
            error_str = str(e).lower()
            if "model" in error_str and ("not found" in error_str or "404" in error_str):
                return "AI model not found. Please check your API configuration. For now, you can use direct task commands like 'Add a task to buy groceries' or 'Show my tasks'."
            elif "api key" in error_str or "unauthorized" in error_str or "permission" in error_str:
                # This means API key issue but we don't expose the actual error
                return "AI service temporarily unavailable due to API configuration. You can still use task commands like 'Add a task to buy groceries' or 'Show my tasks'. Contact admin to check API key configuration."
            elif "quota" in error_str or "billing" in error_str:
                return "AI service temporarily unavailable due to quota limits. You can still use task commands like 'Add a task to buy groceries' or 'Show my tasks'."

            return "AI service temporarily unavailable. You can still use task commands like 'Add a task to buy groceries' or 'Show my tasks'."

    def can_process_naturally(self, message: str) -> bool:
        """
        Determine if the message can be processed naturally with AI
        """
        # For now, we'll say any message can be processed by AI
        # In the future, we could have more sophisticated logic
        return True

# Global instance
gemini_service = GeminiService()