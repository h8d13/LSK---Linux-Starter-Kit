import logging

# Set up basic logging config
logging.basicConfig(
   level=logging.DEBUG,  # Set root level to DEBUG
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create logger for this module
logger = logging.getLogger(__name__)

def process_user_data(users):
   logger.info("Starting user data processing")  # High-level flow
   
   processed_users = []
   for user in users:
       try:
           logger.debug(f"Processing user: {user['id']}")  # Detailed debug info
           
           # Validate email
           if 'email' not in user:
               logger.warning(f"User {user['id']} has no email")
               continue
               
           # Process user data
           logger.debug(f"Validating email: {user['email']}")  # Detailed steps
           processed_users.append(user)
           
       except KeyError as e:
           logger.error(f"Missing required field: {e}")
       except Exception as e:
           logger.critical(f"Unexpected error processing user: {e}")
   
   logger.info(f"Completed processing {len(processed_users)} users")  # High-level result
   return processed_users

# Example usage
users = [
   {'id': 1, 'email': 'user1@example.com'},
   {'id': 2},  # Missing email
   {'id': 3, 'email': 'user3@example.com'}
]

results = process_user_data(users)