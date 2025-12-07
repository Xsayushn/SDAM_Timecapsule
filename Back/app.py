# # from flask import Flask, request, jsonify, send_file
# # from flask_cors import CORS
# # import json
# # import os
# # import uuid
# # from datetime import datetime
# # from pathlib import Path

# # app = Flask(__name__)
# # CORS(app)

# # class CapsuleStorage:
# #     def __init__(self, storage_dir="capsules", media_dir="media"):
# #         self.storage_dir = Path(storage_dir)
# #         self.media_dir = self.storage_dir / media_dir
# #         self.storage_dir.mkdir(exist_ok=True)
# #         self.media_dir.mkdir(exist_ok=True)
    
# #     def save_capsule(self, capsule_data):
# #         """Save a new time capsule"""
# #         capsule_id = str(uuid.uuid4())
# #         capsule_data['id'] = capsule_id
# #         capsule_data['created_at'] = datetime.now().isoformat()
# #         capsule_data['status'] = 'locked'
        
# #         # Handle file uploads
# #         if 'media_files' in capsule_data and capsule_data['media_files']:
# #             saved_files = []
# #             for file_data in capsule_data['media_files']:
# #                 filename = self.save_media_file(file_data)
# #                 saved_files.append({
# #                     'filename': filename,
# #                     'original_name': file_data['filename'],
# #                     'type': file_data['type']
# #                 })
# #             capsule_data['media_files'] = saved_files
# #         else:
# #             capsule_data['media_files'] = []
        
# #         # Save capsule metadata
# #         capsule_file = self.storage_dir / f"{capsule_id}.json"
# #         with open(capsule_file, 'w') as f:
# #             json.dump(capsule_data, f, indent=2)
        
# #         return capsule_id
    
# #     def save_media_file(self, file_data):
# #         """Save media file and return filename"""
# #         filename = f"{uuid.uuid4()}_{file_data['filename']}"
# #         filepath = self.media_dir / filename
        
# #         # Handle base64 encoded files
# #         if isinstance(file_data['content'], str) and file_data['content'].startswith('data:'):
# #             import base64
# #             header, encoded = file_data['content'].split(',', 1)
# #             file_content = base64.b64decode(encoded)
# #         else:
# #             file_content = file_data['content']
        
# #         with open(filepath, 'wb') as f:
# #             f.write(file_content)
        
# #         return filename
    
# #     def get_capsule(self, capsule_id):
# #         """Get a specific capsule"""
# #         capsule_file = self.storage_dir / f"{capsule_id}.json"
# #         if not capsule_file.exists():
# #             return None
        
# #         with open(capsule_file, 'r') as f:
# #             return json.load(f)
    
# #     def get_all_capsules(self):
# #         """Get all capsules"""
# #         capsules = []
# #         for file in self.storage_dir.glob("*.json"):
# #             try:
# #                 with open(file, 'r') as f:
# #                     capsule_data = json.load(f)
# #                     capsules.append(capsule_data)
# #             except Exception as e:
# #                 print(f"Error reading capsule file {file}: {e}")
        
# #         # Sort by delivery date
# #         capsules.sort(key=lambda x: x.get('delivery_date', ''))
# #         return capsules
    
# #     def delete_capsule(self, capsule_id):
# #         """Delete a capsule"""
# #         capsule_file = self.storage_dir / f"{capsule_id}.json"
# #         if capsule_file.exists():
# #             # Also delete associated media files
# #             capsule = self.get_capsule(capsule_id)
# #             if capsule and 'media_files' in capsule:
# #                 for media_file in capsule['media_files']:
# #                     media_path = self.media_dir / media_file['filename']
# #                     if media_path.exists():
# #                         media_path.unlink()
            
# #             capsule_file.unlink()
# #             return True
# #         return False
    
# #     def get_media_file(self, filename):
# #         """Get media file path"""
# #         filepath = self.media_dir / filename
# #         if filepath.exists():
# #             return filepath
# #         return None

# # storage = CapsuleStorage()

# # @app.route('/api/capsules', methods=['GET'])
# # def get_capsules():
# #     """Get all time capsules"""
# #     try:
# #         capsules = storage.get_all_capsules()
# #         return jsonify(capsules)
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @app.route('/api/capsules', methods=['POST'])
# # def create_capsule():
# #     """Create a new time capsule"""
# #     try:
# #         capsule_data = request.json
        
# #         # Validate required fields
# #         required_fields = ['title', 'message', 'delivery_date', 'recipient_type']
# #         for field in required_fields:
# #             if field not in capsule_data:
# #                 return jsonify({'error': f'Missing required field: {field}'}), 400
        
# #         # Save the capsule
# #         capsule_id = storage.save_capsule(capsule_data)
# #         return jsonify({'id': capsule_id, 'message': 'Capsule created successfully'})
    
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @app.route('/api/capsules/<capsule_id>', methods=['GET'])
# # def get_capsule(capsule_id):
# #     """Get a specific capsule"""
# #     try:
# #         capsule = storage.get_capsule(capsule_id)
# #         if capsule:
# #             return jsonify(capsule)
# #         return jsonify({'error': 'Capsule not found'}), 404
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @app.route('/api/capsules/<capsule_id>', methods=['DELETE'])
# # def delete_capsule(capsule_id):
# #     """Delete a capsule"""
# #     try:
# #         success = storage.delete_capsule(capsule_id)
# #         if success:
# #             return jsonify({'message': 'Capsule deleted successfully'})
# #         return jsonify({'error': 'Capsule not found'}), 404
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @app.route('/api/media/<filename>')
# # def get_media(filename):
# #     """Serve media files"""
# #     try:
# #         filepath = storage.get_media_file(filename)
# #         if filepath:
# #             return send_file(filepath)
# #         return jsonify({'error': 'File not found'}), 404
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @app.route('/api/health')
# # def health_check():
# #     """Health check endpoint"""
# #     return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# # if __name__ == '__main__':
# #     print("Time Capsule Backend Server Started!")
# #     print("API running on: http://localhost:5000")
# #     print("Health check: http://localhost:5000/api/health")
# #     app.run(debug=True, port=5000)
# # from flask import Flask, request, jsonify, send_file
# # from flask_cors import CORS
# # from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# # from werkzeug.security import generate_password_hash, check_password_hash
# # import json
# # import os
# # import uuid
# # import smtplib
# # from datetime import datetime, timedelta
# # from pathlib import Path
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
# # import threading

# # app = Flask(__name__)
# # app.config['JWT_SECRET_KEY'] = 'your-super-secret-jwt-key-change-in-production-2024'
# # app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
# # CORS(app)
# # jwt = JWTManager(app)

# # # Email configuration (Update these with your email details)
# # EMAIL_CONFIG = {
# #     'smtp_server': 'smtp.gmail.com',
# #     'smtp_port': 587,
# #     'email_address': 'your-email@gmail.com',  # Change this to your email
# #     'email_password': 'your-app-password'     # Change this to your app password
# # }

# # class UserStorage:
# #     def __init__(self, storage_dir="users"):
# #         self.storage_dir = Path(storage_dir)
# #         self.storage_dir.mkdir(exist_ok=True)
    
# #     def create_user(self, user_data):
# #         user_id = str(uuid.uuid4())
# #         user_data['id'] = user_id
# #         user_data['created_at'] = datetime.now().isoformat()
# #         user_data['password'] = generate_password_hash(user_data['password'])
        
# #         user_file = self.storage_dir / f"{user_id}.json"
# #         with open(user_file, 'w') as f:
# #             json.dump(user_data, f, indent=2)
        
# #         return user_id
    
# #     def get_user_by_email(self, email):
# #         for file in self.storage_dir.glob("*.json"):
# #             with open(file, 'r') as f:
# #                 user_data = json.load(f)
# #                 if user_data.get('email') == email:
# #                     return user_data
# #         return None
    
# #     def get_user_by_id(self, user_id):
# #         user_file = self.storage_dir / f"{user_id}.json"
# #         if user_file.exists():
# #             with open(user_file, 'r') as f:
# #                 return json.load(f)
# #         return None

# # class CapsuleStorage:
# #     def __init__(self, storage_dir="capsules", media_dir="media"):
# #         self.storage_dir = Path(storage_dir)
# #         self.media_dir = self.storage_dir / media_dir
# #         self.storage_dir.mkdir(exist_ok=True)
# #         self.media_dir.mkdir(exist_ok=True)
    
# #     def save_capsule(self, capsule_data):
# #         capsule_id = str(uuid.uuid4())
# #         capsule_data['id'] = capsule_id
# #         capsule_data['created_at'] = datetime.now().isoformat()
# #         capsule_data['status'] = 'locked'
        
# #         # Handle file uploads
# #         if 'media_files' in capsule_data and capsule_data['media_files']:
# #             saved_files = []
# #             for file_data in capsule_data['media_files']:
# #                 filename = self.save_media_file(file_data)
# #                 saved_files.append({
# #                     'filename': filename,
# #                     'original_name': file_data['filename'],
# #                     'type': file_data['type']
# #                 })
# #             capsule_data['media_files'] = saved_files
# #         else:
# #             capsule_data['media_files'] = []
        
# #         capsule_file = self.storage_dir / f"{capsule_id}.json"
# #         with open(capsule_file, 'w') as f:
# #             json.dump(capsule_data, f, indent=2)
        
# #         return capsule_id
    
# #     def save_media_file(self, file_data):
# #         filename = f"{uuid.uuid4()}_{file_data['filename']}"
# #         filepath = self.media_dir / filename
        
# #         if isinstance(file_data['content'], str) and file_data['content'].startswith('data:'):
# #             import base64
# #             header, encoded = file_data['content'].split(',', 1)
# #             file_content = base64.b64decode(encoded)
# #         else:
# #             file_content = file_data['content']
        
# #         with open(filepath, 'wb') as f:
# #             f.write(file_content)
        
# #         return filename
    
# #     def get_user_capsules(self, user_id):
# #         capsules = []
# #         for file in self.storage_dir.glob("*.json"):
# #             try:
# #                 with open(file, 'r') as f:
# #                     capsule_data = json.load(f)
# #                     if capsule_data.get('user_id') == user_id:
# #                         capsules.append(capsule_data)
# #             except Exception as e:
# #                 print(f"Error reading capsule file {file}: {e}")
        
# #         capsules.sort(key=lambda x: x.get('delivery_date', ''))
# #         return capsules
    
# #     def search_capsules(self, user_id, query=None, category=None, tags=None, status=None):
# #         capsules = self.get_user_capsules(user_id)
        
# #         if query:
# #             capsules = [c for c in capsules if 
# #                        query.lower() in c.get('title', '').lower() or 
# #                        query.lower() in c.get('message', '').lower()]
        
# #         if category:
# #             capsules = [c for c in capsules if c.get('category') == category]
        
# #         if tags:
# #             capsule_tags = set(tags)
# #             capsules = [c for c in capsules if 
# #                        capsule_tags.issubset(set(c.get('tags', [])))]
        
# #         if status:
# #             capsules = [c for c in capsules if c.get('status') == status]
        
# #         return capsules
    
# #     def get_capsule(self, capsule_id):
# #         capsule_file = self.storage_dir / f"{capsule_id}.json"
# #         if not capsule_file.exists():
# #             return None
        
# #         with open(capsule_file, 'r') as f:
# #             return json.load(f)
    
# #     def update_capsule(self, capsule_id, updates):
# #         capsule = self.get_capsule(capsule_id)
# #         if not capsule:
# #             return None
        
# #         capsule.update(updates)
# #         capsule_file = self.storage_dir / f"{capsule_id}.json"
# #         with open(capsule_file, 'w') as f:
# #             json.dump(capsule, f, indent=2)
        
# #         return capsule
    
# #     def delete_capsule(self, capsule_id):
# #         capsule_file = self.storage_dir / f"{capsule_id}.json"
# #         if capsule_file.exists():
# #             capsule = self.get_capsule(capsule_id)
# #             if capsule and 'media_files' in capsule:
# #                 for media_file in capsule['media_files']:
# #                     media_path = self.media_dir / media_file['filename']
# #                     if media_path.exists():
# #                         media_path.unlink()
# #             capsule_file.unlink()
# #             return True
# #         return False
    
# #     def get_media_file(self, filename):
# #         filepath = self.media_dir / filename
# #         if filepath.exists():
# #             return filepath
# #         return None

# # class EmailService:
# #     @staticmethod
# #     def send_capsule_notification(recipient_emails, capsule_title, delivery_date, open_url):
# #         """Send email notification when capsule is ready"""
# #         try:
# #             # For demo purposes, we'll just print the email details
# #             # In production, you would send actual emails
# #             print("=" * 50)
# #             print("📧 EMAIL NOTIFICATION (Simulated)")
# #             print(f"To: {', '.join(recipient_emails)}")
# #             print(f"Subject: 🎉 Your Time Capsule '{capsule_title}' is Ready!")
# #             print(f"Message: Your time capsule scheduled for {delivery_date} is ready to open!")
# #             print(f"Open URL: {open_url}")
# #             print("=" * 50)
            
# #             # Uncomment and configure the code below for real email sending:
# #             """
# #             message = MIMEMultipart()
# #             message['From'] = EMAIL_CONFIG['email_address']
# #             message['To'] = ', '.join(recipient_emails)
# #             message['Subject'] = f'🎉 Your Time Capsule "{capsule_title}" is Ready!'
            
# #             body = f'''
# #             <html>
# #             <body>
# #                 <h2>Your Time Capsule is Ready! 🎁</h2>
# #                 <p>Your time capsule "<strong>{capsule_title}</strong>" is now ready to be opened!</p>
# #                 <p>It was scheduled for delivery on: {delivery_date}</p>
# #                 <p><a href="{open_url}">Click here to open your time capsule</a></p>
# #                 <br>
# #                 <p>Best regards,<br>Time Capsule Team</p>
# #             </body>
# #             </html>
# #             '''
            
# #             message.attach(MIMEText(body, 'html'))
            
# #             server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
# #             server.starttls()
# #             server.login(EMAIL_CONFIG['email_address'], EMAIL_CONFIG['email_password'])
# #             server.send_message(message)
# #             server.quit()
# #             """
            
# #             return True
            
# #         except Exception as e:
# #             print(f"Email error: {e}")
# #             return False

# # class CapsuleScheduler:
# #     def __init__(self, capsule_storage, user_storage):
# #         self.capsule_storage = capsule_storage
# #         self.user_storage = user_storage
    
# #     def check_due_capsules(self):
# #         """Check for capsules that are due and send notifications"""
# #         all_capsules = []
# #         for file in self.capsule_storage.storage_dir.glob("*.json"):
# #             with open(file, 'r') as f:
# #                 all_capsules.append(json.load(f))
        
# #         today = datetime.now().date()
        
# #         for capsule in all_capsules:
# #             if capsule.get('status') == 'locked':
# #                 try:
# #                     delivery_date = datetime.fromisoformat(capsule['delivery_date']).date()
# #                     if delivery_date <= today:
# #                         # Mark as ready
# #                         self.capsule_storage.update_capsule(capsule['id'], {'status': 'ready'})
# #                         print(f"📦 Capsule '{capsule['title']}' is now ready!")
                        
# #                         # Prepare recipient emails
# #                         recipient_emails = []
                        
# #                         # Get sender's email for notification
# #                         user = self.user_storage.get_user_by_id(capsule['user_id'])
# #                         if user:
# #                             recipient_emails.append(user['email'])
                        
# #                         # Add other recipients if any
# #                         if capsule.get('recipient_type') == 'multiple' and 'recipients' in capsule:
# #                             recipient_emails.extend(capsule['recipients'])
# #                         elif capsule.get('recipient_type') == 'other' and 'recipient_email' in capsule:
# #                             recipient_emails.append(capsule['recipient_email'])
                        
# #                         # Send email notification
# #                         if recipient_emails:
# #                             open_url = f"http://localhost:3000/capsule/{capsule['id']}"
# #                             EmailService.send_capsule_notification(
# #                                 recipient_emails,
# #                                 capsule['title'],
# #                                 capsule['delivery_date'],
# #                                 open_url
# #                             )
                            
# #                 except Exception as e:
# #                     print(f"Error processing capsule {capsule.get('id')}: {e}")

# # # Initialize storage
# # user_storage = UserStorage()
# # capsule_storage = CapsuleStorage()
# # scheduler = CapsuleScheduler(capsule_storage, user_storage)

# # # Auth Routes
# # @app.route('/api/auth/register', methods=['POST'])
# # def register():
# #     try:
# #         user_data = request.json
# #         required_fields = ['email', 'password', 'name']
        
# #         for field in required_fields:
# #             if field not in user_data:
# #                 return jsonify({'error': f'Missing required field: {field}'}), 400
        
# #         if user_storage.get_user_by_email(user_data['email']):
# #             return jsonify({'error': 'User already exists'}), 400
        
# #         user_id = user_storage.create_user(user_data)
# #         access_token = create_access_token(identity=user_id)
        
# #         return jsonify({
# #             'message': 'User created successfully',
# #             'access_token': access_token,
# #             'user': {
# #                 'id': user_id,
# #                 'email': user_data['email'],
# #                 'name': user_data['name']
# #             }
# #         })
    
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @app.route('/api/auth/login', methods=['POST'])
# # def login():
# #     try:
# #         credentials = request.json
# #         if not credentials or 'email' not in credentials or 'password' not in credentials:
# #             return jsonify({'error': 'Email and password required'}), 400
        
# #         user = user_storage.get_user_by_email(credentials['email'])
# #         if not user or not check_password_hash(user['password'], credentials['password']):
# #             return jsonify({'error': 'Invalid credentials'}), 401
        
# #         access_token = create_access_token(identity=user['id'])
        
# #         return jsonify({
# #             'message': 'Login successful',
# #             'access_token': access_token,
# #             'user': {
# #                 'id': user['id'],
# #                 'email': user['email'],
# #                 'name': user['name']
# #             }
# #         })
    
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @app.route('/api/auth/me', methods=['GET'])
# # @jwt_required()
# # def get_current_user():
# #     try:
# #         user_id = get_jwt_identity()
# #         user = user_storage.get_user_by_id(user_id)
# #         if not user:
# #             return jsonify({'error': 'User not found'}), 404
        
# #         return jsonify({
# #             'id': user['id'],
# #             'email': user['email'],
# #             'name': user['name'],
# #             'created_at': user['created_at']
# #         })
    
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # # Enhanced Capsule Routes
# # @app.route('/api/capsules', methods=['GET'])
# # @jwt_required()
# # def get_capsules():
# #     try:
# #         user_id = get_jwt_identity()
# #         query = request.args.get('q')
# #         category = request.args.get('category')
# #         tags = request.args.getlist('tags')
# #         status = request.args.get('status')
        
# #         if any([query, category, tags, status]):
# #             capsules = capsule_storage.search_capsules(user_id, query, category, tags, status)
# #         else:
# #             capsules = capsule_storage.get_user_capsules(user_id)
        
# #         return jsonify(capsules)
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @app.route('/api/capsules', methods=['POST'])
# # @jwt_required()
# # def create_capsule():
# #     try:
# #         user_id = get_jwt_identity()
# #         capsule_data = request.json
# #         capsule_data['user_id'] = user_id
        
# #         required_fields = ['title', 'message', 'delivery_date', 'recipient_type']
# #         for field in required_fields:
# #             if field not in capsule_data:
# #                 return jsonify({'error': f'Missing required field: {field}'}), 400
        
# #         # Handle multiple recipients
# #         if capsule_data['recipient_type'] == 'multiple' and 'recipients' not in capsule_data:
# #             return jsonify({'error': 'Missing recipients for multiple recipients'}), 400
        
# #         capsule_id = capsule_storage.save_capsule(capsule_data)
# #         return jsonify({'id': capsule_id, 'message': 'Capsule created successfully'})
    
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @app.route('/api/capsules/<capsule_id>', methods=['GET'])
# # @jwt_required()
# # def get_capsule(capsule_id):
# #     try:
# #         user_id = get_jwt_identity()
# #         capsule = capsule_storage.get_capsule(capsule_id)
        
# #         if not capsule or capsule.get('user_id') != user_id:
# #             return jsonify({'error': 'Capsule not found'}), 404
        
# #         return jsonify(capsule)
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @app.route('/api/capsules/<capsule_id>', methods=['PUT'])
# # @jwt_required()
# # def update_capsule(capsule_id):
# #     try:
# #         user_id = get_jwt_identity()
# #         capsule = capsule_storage.get_capsule(capsule_id)
        
# #         if not capsule or capsule.get('user_id') != user_id:
# #             return jsonify({'error': 'Capsule not found'}), 404
        
# #         updates = request.json
# #         updated_capsule = capsule_storage.update_capsule(capsule_id, updates)
        
# #         return jsonify(updated_capsule)
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @app.route('/api/capsules/<capsule_id>', methods=['DELETE'])
# # @jwt_required()
# # def delete_capsule(capsule_id):
# #     try:
# #         user_id = get_jwt_identity()
# #         capsule = capsule_storage.get_capsule(capsule_id)
        
# #         if not capsule or capsule.get('user_id') != user_id:
# #             return jsonify({'error': 'Capsule not found'}), 404
        
# #         success = capsule_storage.delete_capsule(capsule_id)
# #         if success:
# #             return jsonify({'message': 'Capsule deleted successfully'})
# #         return jsonify({'error': 'Capsule not found'}), 404
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @app.route('/api/capsules/categories', methods=['GET'])
# # @jwt_required()
# # def get_categories():
# #     categories = ['personal', 'birthday', 'anniversary', 'graduation', 'travel', 'goals', 'other']
# #     return jsonify(categories)

# # @app.route('/api/media/<filename>')
# # @jwt_required()
# # def get_media(filename):
# #     try:
# #         filepath = capsule_storage.get_media_file(filename)
# #         if filepath:
# #             return send_file(filepath)
# #         return jsonify({'error': 'File not found'}), 404
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @app.route('/api/health')
# # def health_check():
# #     return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# # # Background scheduler thread
# # def run_scheduler():
# #     """Background thread to check for due capsules"""
# #     while True:
# #         try:
# #             scheduler.check_due_capsules()
# #         except Exception as e:
# #             print(f"Scheduler error: {e}")
# #         threading.Event().wait(60)  # Check every minute for demo

# # # Start scheduler when app starts
# # scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
# # scheduler_thread.start()

# # if __name__ == '__main__':
# #     print("🚀 Enhanced Time Capsule Backend Started!")
# #     print("📧 Features: Authentication, Email Notifications, Search, Categories, Multiple Recipients")
# #     print("📍 API: http://localhost:5000")
# #     print("🔑 JWT Authentication: Enabled")
# #     print("📬 Email: Simulated (check console for notifications)")
# #     app.run(debug=True, port=5000)

# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from werkzeug.security import generate_password_hash, check_password_hash
# import json
# import os
# import uuid
# import smtplib
# from datetime import datetime, timedelta
# from pathlib import Path
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import threading

# app = Flask(__name__)
# app.config['JWT_SECRET_KEY'] = 'your-super-secret-jwt-key-change-in-production-2024'
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
# CORS(app)
# jwt = JWTManager(app)


# EMAIL_CONFIG = {
#     'smtp_server': 'smtp.gmail.com',  
#     'smtp_port': 587,
#     'email_address': 'kingayush1508@gmail.com',  
#     'email_password': 'vmxd lntu ynkv aoex' 
# }

# class CapsuleStorage:
#     # ... (keep all existing functions)
    
#     def get_received_capsules(self, user_email):
#         """Get capsules where user is a recipient"""
#         received_capsules = []
#         for file in self.storage_dir.glob("*.json"):
#             try:
#                 with open(file, 'r') as f:
#                     capsule_data = json.load(f)
                    
#                     # Check if user is a recipient
#                     if capsule_data.get('recipient_type') == 'other' and capsule_data.get('recipient_email') == user_email:
#                         received_capsules.append(capsule_data)
#                     elif capsule_data.get('recipient_type') == 'multiple' and user_email in capsule_data.get('recipients', []):
#                         received_capsules.append(capsule_data)
                        
#             except Exception as e:
#                 print(f"Error reading capsule file {file}: {e}")
        
#         received_capsules.sort(key=lambda x: x.get('delivery_date', ''))
#         return received_capsules

# # Add these new routes after your existing capsule routes
# @app.route('/api/capsules/received', methods=['GET'])
# @jwt_required()
# def get_received_capsules():
#     """Get capsules where current user is a recipient"""
#     try:
#         user_id = get_jwt_identity()
#         user = user_storage.get_user_by_id(user_id)
#         if not user:
#             return jsonify({'error': 'User not found'}), 404
        
#         received_capsules = capsule_storage.get_received_capsules(user['email'])
#         return jsonify(received_capsules)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/capsules/sent', methods=['GET'])
# @jwt_required()
# def get_sent_capsules():
#     """Get capsules sent by current user"""
#     try:
#         user_id = get_jwt_identity()
#         capsules = capsule_storage.get_user_capsules(user_id)
#         return jsonify(capsules)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/capsules/shared/<capsule_id>', methods=['GET'])
# def get_shared_capsule(capsule_id):
#     """Public endpoint to view shared capsules (no auth required)"""
#     try:
#         capsule = capsule_storage.get_capsule(capsule_id)
        
#         if not capsule:
#             return jsonify({'error': 'Capsule not found'}), 404
        
#         # Only return capsule if it's ready to open
#         if capsule.get('status') != 'ready':
#             return jsonify({'error': 'Capsule is not ready yet'}), 403
        
#         # Return basic capsule info for sharing
#         shared_capsule = {
#             'id': capsule['id'],
#             'title': capsule['title'],
#             'message': capsule['message'],
#             'delivery_date': capsule['delivery_date'],
#             'created_at': capsule['created_at'],
#             'sender_name': 'A Friend',  # Don't expose sender details
#             'media_files': capsule.get('media_files', [])
#         }
        
#         return jsonify(shared_capsule)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# class UserStorage:
#     def __init__(self, storage_dir="users"):
#         self.storage_dir = Path(storage_dir)
#         self.storage_dir.mkdir(exist_ok=True)
    
#     def create_user(self, user_data):
#         user_id = str(uuid.uuid4())
#         user_data['id'] = user_id
#         user_data['created_at'] = datetime.now().isoformat()
#         user_data['password'] = generate_password_hash(user_data['password'])
        
#         user_file = self.storage_dir / f"{user_id}.json"
#         with open(user_file, 'w') as f:
#             json.dump(user_data, f, indent=2)
        
#         return user_id
    
#     def get_user_by_email(self, email):
#         for file in self.storage_dir.glob("*.json"):
#             with open(file, 'r') as f:
#                 user_data = json.load(f)
#                 if user_data.get('email') == email:
#                     return user_data
#         return None
    
#     def get_user_by_id(self, user_id):
#         user_file = self.storage_dir / f"{user_id}.json"
#         if user_file.exists():
#             with open(user_file, 'r') as f:
#                 return json.load(f)
#         return None

# class CapsuleStorage:
#     def __init__(self, storage_dir="capsules", media_dir="media"):
#         self.storage_dir = Path(storage_dir)
#         self.media_dir = self.storage_dir / media_dir
#         self.storage_dir.mkdir(exist_ok=True)
#         self.media_dir.mkdir(exist_ok=True)
    
#     def save_capsule(self, capsule_data):
#         capsule_id = str(uuid.uuid4())
#         capsule_data['id'] = capsule_id
#         capsule_data['created_at'] = datetime.now().isoformat()
#         capsule_data['status'] = 'locked'
        
#         # Handle file uploads
#         if 'media_files' in capsule_data and capsule_data['media_files']:
#             saved_files = []
#             for file_data in capsule_data['media_files']:
#                 filename = self.save_media_file(file_data)
#                 saved_files.append({
#                     'filename': filename,
#                     'original_name': file_data['filename'],
#                     'type': file_data['type']
#                 })
#             capsule_data['media_files'] = saved_files
#         else:
#             capsule_data['media_files'] = []
        
#         capsule_file = self.storage_dir / f"{capsule_id}.json"
#         with open(capsule_file, 'w') as f:
#             json.dump(capsule_data, f, indent=2)
        
#         return capsule_id
    
#     def save_media_file(self, file_data):
#         filename = f"{uuid.uuid4()}_{file_data['filename']}"
#         filepath = self.media_dir / filename
        
#         if isinstance(file_data['content'], str) and file_data['content'].startswith('data:'):
#             import base64
#             header, encoded = file_data['content'].split(',', 1)
#             file_content = base64.b64decode(encoded)
#         else:
#             file_content = file_data['content']
        
#         with open(filepath, 'wb') as f:
#             f.write(file_content)
        
#         return filename
    
#     def get_user_capsules(self, user_id):
#         capsules = []
#         for file in self.storage_dir.glob("*.json"):
#             try:
#                 with open(file, 'r') as f:
#                     capsule_data = json.load(f)
#                     if capsule_data.get('user_id') == user_id:
#                         capsules.append(capsule_data)
#             except Exception as e:
#                 print(f"Error reading capsule file {file}: {e}")
        
#         capsules.sort(key=lambda x: x.get('delivery_date', ''))
#         return capsules
    
#     def search_capsules(self, user_id, query=None, category=None, tags=None, status=None):
#         capsules = self.get_user_capsules(user_id)
        
#         if query:
#             capsules = [c for c in capsules if 
#                        query.lower() in c.get('title', '').lower() or 
#                        query.lower() in c.get('message', '').lower()]
        
#         if category:
#             capsules = [c for c in capsules if c.get('category') == category]
        
#         if tags:
#             capsule_tags = set(tags)
#             capsules = [c for c in capsules if 
#                        capsule_tags.issubset(set(c.get('tags', [])))]
        
#         if status:
#             capsules = [c for c in capsules if c.get('status') == status]
        
#         return capsules
    
#     def get_capsule(self, capsule_id):
#         capsule_file = self.storage_dir / f"{capsule_id}.json"
#         if not capsule_file.exists():
#             return None
        
#         with open(capsule_file, 'r') as f:
#             return json.load(f)
    
#     def update_capsule(self, capsule_id, updates):
#         capsule = self.get_capsule(capsule_id)
#         if not capsule:
#             return None
        
#         capsule.update(updates)
#         capsule_file = self.storage_dir / f"{capsule_id}.json"
#         with open(capsule_file, 'w') as f:
#             json.dump(capsule, f, indent=2)
        
#         return capsule
    
#     def delete_capsule(self, capsule_id):
#         capsule_file = self.storage_dir / f"{capsule_id}.json"
#         if capsule_file.exists():
#             capsule = self.get_capsule(capsule_id)
#             if capsule and 'media_files' in capsule:
#                 for media_file in capsule['media_files']:
#                     media_path = self.media_dir / media_file['filename']
#                     if media_path.exists():
#                         media_path.unlink()
#             capsule_file.unlink()
#             return True
#         return False
    
#     def get_media_file(self, filename):
#         filepath = self.media_dir / filename
#         if filepath.exists():
#             return filepath
#         return None

# class EmailService:
#     @staticmethod
#     def send_capsule_notification(recipient_emails, capsule_title, delivery_date, capsule_id):
#         """Send REAL email notification when capsule is ready"""
#         try:
#             # Create message
#             message = MIMEMultipart()
#             message['From'] = EMAIL_CONFIG['email_address']
#             message['To'] = ', '.join(recipient_emails)
#             message['Subject'] = f'🎉 Your Time Capsule "{capsule_title}" is Ready!'
            
#             # Create email body
#             body = f"""
#             <!DOCTYPE html>
#             <html>
#             <head>
#                 <style>
#                     body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
#                     .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
#                     .header {{ background: linear-gradient(135deg, #696FC7, #A7AAE1); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
#                     .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
#                     .button {{ display: inline-block; background: #696FC7; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
#                     .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 14px; }}
#                 </style>
#             </head>
#             <body>
#                 <div class="container">
#                     <div class="header">
#                         <h1>🎁 Your Time Capsule is Ready!</h1>
#                     </div>
#                     <div class="content">
#                         <h2>Hello!</h2>
#                         <p>Your time capsule <strong>"{capsule_title}"</strong> is now ready to be opened!</p>
#                         <p>It was scheduled for delivery on: <strong>{delivery_date}</strong></p>
#                         <p>This message was sent from the future by your past self! ✨</p>
                        
#                         <div style="text-align: center;">
#                             <a href="http://localhost:3000" class="button">Open Your Time Capsule</a>
#                         </div>
                        
#                         <p><em>Note: You'll need to log in to your Time Capsule account to view this capsule.</em></p>
#                     </div>
#                     <div class="footer">
#                         <p>Sent with 💌 from Time Capsule App</p>
#                         <p>This is an automated message, please do not reply.</p>
#                     </div>
#                 </div>
#             </body>
#             </html>
#             """
            
#             message.attach(MIMEText(body, 'html'))
            
#             # Send email
#             print(f"📧 Attempting to send email to: {recipient_emails}")
            
#             server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
#             server.starttls()
            
#             # Login with email credentials
#             server.login(EMAIL_CONFIG['email_address'], EMAIL_CONFIG['email_password'])
            
#             # Send the email
#             server.send_message(message)
#             server.quit()
            
#             print(f"✅ Email successfully sent to: {recipient_emails}")
#             return True
            
#         except Exception as e:
#             print(f"❌ Failed to send email: {str(e)}")
#             # Fallback to console notification
#             print("=" * 60)
#             print("📧 EMAIL NOTIFICATION (Failed to send - showing details)")
#             print(f"To: {', '.join(recipient_emails)}")
#             print(f"Subject: 🎉 Your Time Capsule '{capsule_title}' is Ready!")
#             print(f"Capsule ID: {capsule_id}")
#             print(f"Scheduled for: {delivery_date}")
#             print("=" * 60)
#             return False

# class CapsuleScheduler:
#     def __init__(self, capsule_storage, user_storage):
#         self.capsule_storage = capsule_storage
#         self.user_storage = user_storage
    
#     def check_due_capsules(self):
#         """Check for capsules that are due and send REAL notifications"""
#         all_capsules = []
#         for file in self.capsule_storage.storage_dir.glob("*.json"):
#             with open(file, 'r') as f:
#                 all_capsules.append(json.load(f))
        
#         today = datetime.now().date()
#         print(f"🔍 Checking for due capsules... ({len(all_capsules)} total capsules)")
        
#         for capsule in all_capsules:
#             if capsule.get('status') == 'locked':
#                 try:
#                     delivery_date = datetime.fromisoformat(capsule['delivery_date']).date()
#                     if delivery_date <= today:
#                         print(f"🎯 Capsule '{capsule['title']}' is due! Sending notifications...")
                        
#                         # Mark as ready
#                         self.capsule_storage.update_capsule(capsule['id'], {'status': 'ready'})
                        
#                         # Prepare recipient emails
#                         recipient_emails = []
                        
#                         # Get sender's email for notification
#                         user = self.user_storage.get_user_by_id(capsule['user_id'])
#                         if user:
#                             recipient_emails.append(user['email'])
#                             print(f"👤 Added sender: {user['email']}")
                        
#                         # Add other recipients if any
#                         if capsule.get('recipient_type') == 'multiple' and 'recipients' in capsule:
#                             recipient_emails.extend(capsule['recipients'])
#                             print(f"👥 Added multiple recipients: {capsule['recipients']}")
#                         elif capsule.get('recipient_type') == 'other' and 'recipient_email' in capsule:
#                             recipient_emails.append(capsule['recipient_email'])
#                             print(f"👤 Added recipient: {capsule['recipient_email']}")
                        
#                         # Remove duplicates
#                         recipient_emails = list(set(recipient_emails))
                        
#                         # Send REAL email notification
#                         if recipient_emails and EMAIL_CONFIG['email_password'] != 'your-app-password-here':
#                             EmailService.send_capsule_notification(
#                                 recipient_emails,
#                                 capsule['title'],
#                                 capsule['delivery_date'],
#                                 capsule['id']
#                             )
#                         else:
#                             print("ℹ️  Email not configured or no recipients. Showing notification details:")
#                             print(f"   Capsule: {capsule['title']}")
#                             print(f"   Recipients: {recipient_emails}")
#                             print(f"   Delivery Date: {capsule['delivery_date']}")
                            
#                 except Exception as e:
#                     print(f"❌ Error processing capsule {capsule.get('id')}: {e}")

# # Initialize storage
# user_storage = UserStorage()
# capsule_storage = CapsuleStorage()
# scheduler = CapsuleScheduler(capsule_storage, user_storage)

# # ... (Keep all your existing routes - register, login, capsules, etc.)
# # Auth Routes
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     try:
#         user_data = request.json
#         required_fields = ['email', 'password', 'name']
        
#         for field in required_fields:
#             if field not in user_data:
#                 return jsonify({'error': f'Missing required field: {field}'}), 400
        
#         if user_storage.get_user_by_email(user_data['email']):
#             return jsonify({'error': 'User already exists'}), 400
        
#         user_id = user_storage.create_user(user_data)
#         access_token = create_access_token(identity=user_id)
        
#         return jsonify({
#             'message': 'User created successfully',
#             'access_token': access_token,
#             'user': {
#                 'id': user_id,
#                 'email': user_data['email'],
#                 'name': user_data['name']
#             }
#         })
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     try:
#         credentials = request.json
#         if not credentials or 'email' not in credentials or 'password' not in credentials:
#             return jsonify({'error': 'Email and password required'}), 400
        
#         user = user_storage.get_user_by_email(credentials['email'])
#         if not user or not check_password_hash(user['password'], credentials['password']):
#             return jsonify({'error': 'Invalid credentials'}), 401
        
#         access_token = create_access_token(identity=user['id'])
        
#         return jsonify({
#             'message': 'Login successful',
#             'access_token': access_token,
#             'user': {
#                 'id': user['id'],
#                 'email': user['email'],
#                 'name': user['name']
#             }
#         })
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/auth/me', methods=['GET'])
# @jwt_required()
# def get_current_user():
#     try:
#         user_id = get_jwt_identity()
#         user = user_storage.get_user_by_id(user_id)
#         if not user:
#             return jsonify({'error': 'User not found'}), 404
        
#         return jsonify({
#             'id': user['id'],
#             'email': user['email'],
#             'name': user['name'],
#             'created_at': user['created_at']
#         })
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Enhanced Capsule Routes
# @app.route('/api/capsules', methods=['GET'])
# @jwt_required()
# def get_capsules():
#     try:
#         user_id = get_jwt_identity()
#         query = request.args.get('q')
#         category = request.args.get('category')
#         tags = request.args.getlist('tags')
#         status = request.args.get('status')
        
#         if any([query, category, tags, status]):
#             capsules = capsule_storage.search_capsules(user_id, query, category, tags, status)
#         else:
#             capsules = capsule_storage.get_user_capsules(user_id)
        
#         return jsonify(capsules)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/capsules', methods=['POST'])
# @jwt_required()
# def create_capsule():
#     try:
#         user_id = get_jwt_identity()
#         capsule_data = request.json
#         capsule_data['user_id'] = user_id
        
#         required_fields = ['title', 'message', 'delivery_date', 'recipient_type']
#         for field in required_fields:
#             if field not in capsule_data:
#                 return jsonify({'error': f'Missing required field: {field}'}), 400
        
#         # Handle multiple recipients
#         if capsule_data['recipient_type'] == 'multiple' and 'recipients' not in capsule_data:
#             return jsonify({'error': 'Missing recipients for multiple recipients'}), 400
        
#         capsule_id = capsule_storage.save_capsule(capsule_data)
#         return jsonify({'id': capsule_id, 'message': 'Capsule created successfully'})
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/capsules/<capsule_id>', methods=['GET'])
# @jwt_required()
# def get_capsule(capsule_id):
#     try:
#         user_id = get_jwt_identity()
#         capsule = capsule_storage.get_capsule(capsule_id)
        
#         if not capsule or capsule.get('user_id') != user_id:
#             return jsonify({'error': 'Capsule not found'}), 404
        
#         return jsonify(capsule)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/capsules/<capsule_id>', methods=['DELETE'])
# @jwt_required()
# def delete_capsule(capsule_id):
#     try:
#         user_id = get_jwt_identity()
#         capsule = capsule_storage.get_capsule(capsule_id)
        
#         if not capsule or capsule.get('user_id') != user_id:
#             return jsonify({'error': 'Capsule not found'}), 404
        
#         success = capsule_storage.delete_capsule(capsule_id)
#         if success:
#             return jsonify({'message': 'Capsule deleted successfully'})
#         return jsonify({'error': 'Capsule not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/capsules/categories', methods=['GET'])
# @jwt_required()
# def get_categories():
#     categories = ['personal', 'birthday', 'anniversary', 'graduation', 'travel', 'goals', 'other']
#     return jsonify(categories)

# @app.route('/api/media/<filename>')
# @jwt_required()
# def get_media(filename):
#     try:
#         filepath = capsule_storage.get_media_file(filename)
#         if filepath:
#             return send_file(filepath)
#         return jsonify({'error': 'File not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/health')
# def health_check():
#     return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# # Background scheduler thread
# def run_scheduler():
#     """Background thread to check for due capsules"""
#     while True:
#         try:
#             scheduler.check_due_capsules()
#         except Exception as e:
#             print(f"Scheduler error: {e}")
#         threading.Event().wait(60)  # Check every minute

# # Start scheduler when app starts
# scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
# scheduler_thread.start()

# if __name__ == '__main__':
#     print("🚀 Enhanced Time Capsule Backend Started!")
#     print("📧 Features: Authentication, REAL Email Notifications, Search, Categories")
#     print("📍 API: http://localhost:5000")
#     print("🔑 JWT Authentication: Enabled")
    
#     # Check email configuration
#     if EMAIL_CONFIG['email_password'] == 'your-app-password-here':
#         print("⚠️  Email: NOT CONFIGURED - Set EMAIL_PASSWORD in code to enable real emails")
#         print("   Currently showing notifications in console only")
#     else:
#         print("✅ Email: CONFIGURED - Real emails will be sent")
    
#     app.run(debug=True, port=5000)



# new 
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import uuid
import smtplib
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-super-secret-jwt-key-change-in-production-2024'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
CORS(app)
jwt = JWTManager(app)

# Email configuration for Gmail
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email_address': 'kingayush1508@gmail.com',
    'email_password': '@AYUSH4930a'
}

class UserStorage:
    def __init__(self, storage_dir="users"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
    
    def create_user(self, user_data):
        user_id = str(uuid.uuid4())
        user_data['id'] = user_id
        user_data['created_at'] = datetime.now().isoformat()
        user_data['password'] = generate_password_hash(user_data['password'])
        
        user_file = self.storage_dir / f"{user_id}.json"
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        return user_id
    
    def get_user_by_email(self, email):
        """Get user by email address"""
        for file in self.storage_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    user_data = json.load(f)
                    if user_data.get('email') == email:
                        return user_data
            except Exception as e:
                print(f"Error reading user file {file}: {e}")
        return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        user_file = self.storage_dir / f"{user_id}.json"
        if user_file.exists():
            with open(user_file, 'r') as f:
                return json.load(f)
        return None
    
    def update_user(self, user_id, updates):
        """Update user information"""
        user_file = self.storage_dir / f"{user_id}.json"
        if not user_file.exists():
            return None
        
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        # Don't update password directly through this method
        if 'password' in updates:
            if updates['password']:  # Only update if password is provided
                user_data['password'] = generate_password_hash(updates['password'])
            del updates['password']
        
        user_data.update(updates)
        
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        # Remove password from returned data
        user_data.pop('password', None)
        return user_data
    
    def get_all_users(self):
        """Get all users (for debugging/admin purposes)"""
        users = []
        for file in self.storage_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    user_data = json.load(f)
                    user_data.pop('password', None)  # Remove password
                    users.append(user_data)
            except Exception as e:
                print(f"Error reading user file {file}: {e}")
        return users

class CapsuleStorage:
    def __init__(self, storage_dir="capsules", media_dir="media"):
        self.storage_dir = Path(storage_dir)
        self.media_dir = self.storage_dir / media_dir
        self.storage_dir.mkdir(exist_ok=True)
        self.media_dir.mkdir(exist_ok=True)
    
    def save_capsule(self, capsule_data):
        capsule_id = str(uuid.uuid4())
        capsule_data['id'] = capsule_id
        capsule_data['created_at'] = datetime.now().isoformat()
        capsule_data['status'] = 'locked'
        
        # Handle file uploads
        if 'media_files' in capsule_data and capsule_data['media_files']:
            saved_files = []
            for file_data in capsule_data['media_files']:
                filename = self.save_media_file(file_data)
                saved_files.append({
                    'filename': filename,
                    'original_name': file_data['filename'],
                    'type': file_data['type']
                })
            capsule_data['media_files'] = saved_files
        else:
            capsule_data['media_files'] = []
        
        capsule_file = self.storage_dir / f"{capsule_id}.json"
        with open(capsule_file, 'w') as f:
            json.dump(capsule_data, f, indent=2)
        
        return capsule_id
    
    def save_media_file(self, file_data):
        filename = f"{uuid.uuid4()}_{file_data['filename']}"
        filepath = self.media_dir / filename
        
        if isinstance(file_data['content'], str) and file_data['content'].startswith('data:'):
            import base64
            header, encoded = file_data['content'].split(',', 1)
            file_content = base64.b64decode(encoded)
        else:
            file_content = file_data['content']
        
        with open(filepath, 'wb') as f:
            f.write(file_content)
        
        return filename
    
    def get_user_capsules(self, user_id):
        capsules = []
        for file in self.storage_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    capsule_data = json.load(f)
                    if capsule_data.get('user_id') == user_id:
                        capsules.append(capsule_data)
            except Exception as e:
                print(f"Error reading capsule file {file}: {e}")
        
        capsules.sort(key=lambda x: x.get('delivery_date', ''))
        return capsules
    
    def get_received_capsules(self, user_email):
        """Get capsules where user is a recipient"""
        received_capsules = []
        for file in self.storage_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    capsule_data = json.load(f)
                    
                    # Check if user is a recipient
                    if capsule_data.get('recipient_type') == 'other' and capsule_data.get('recipient_email') == user_email:
                        received_capsules.append(capsule_data)
                    elif capsule_data.get('recipient_type') == 'multiple' and user_email in capsule_data.get('recipients', []):
                        received_capsules.append(capsule_data)
                        
            except Exception as e:
                print(f"Error reading capsule file {file}: {e}")
        
        received_capsules.sort(key=lambda x: x.get('delivery_date', ''))
        return received_capsules
    
    def search_capsules(self, user_id, query=None, category=None, tags=None, status=None):
        capsules = self.get_user_capsules(user_id)
        
        if query:
            capsules = [c for c in capsules if 
                       query.lower() in c.get('title', '').lower() or 
                       query.lower() in c.get('message', '').lower()]
        
        if category:
            capsules = [c for c in capsules if c.get('category') == category]
        
        if tags:
            capsule_tags = set(tags)
            capsules = [c for c in capsules if 
                       capsule_tags.issubset(set(c.get('tags', [])))]
        
        if status:
            capsules = [c for c in capsules if c.get('status') == status]
        
        return capsules
    
    def get_capsule(self, capsule_id):
        capsule_file = self.storage_dir / f"{capsule_id}.json"
        if not capsule_file.exists():
            return None
        
        with open(capsule_file, 'r') as f:
            return json.load(f)
    
    def update_capsule(self, capsule_id, updates):
        capsule = self.get_capsule(capsule_id)
        if not capsule:
            return None
        
        capsule.update(updates)
        capsule_file = self.storage_dir / f"{capsule_id}.json"
        with open(capsule_file, 'w') as f:
            json.dump(capsule, f, indent=2)
        
        return capsule
    
    def delete_capsule(self, capsule_id):
        capsule_file = self.storage_dir / f"{capsule_id}.json"
        if capsule_file.exists():
            capsule = self.get_capsule(capsule_id)
            if capsule and 'media_files' in capsule:
                for media_file in capsule['media_files']:
                    media_path = self.media_dir / media_file['filename']
                    if media_path.exists():
                        media_path.unlink()
            capsule_file.unlink()
            return True
        return False
    
    def get_media_file(self, filename):
        filepath = self.media_dir / filename
        if filepath.exists():
            return filepath
        return None
    
    def get_all_capsules(self):
        """Get all capsules (for debugging/scheduler purposes)"""
        capsules = []
        for file in self.storage_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    capsules.append(json.load(f))
            except Exception as e:
                print(f"Error reading capsule file {file}: {e}")
        return capsules

class EmailService:
    @staticmethod
    def send_capsule_notification(recipient_emails, capsule_title, delivery_date, capsule_id, sender_name):
        """Send REAL email notification when capsule is ready"""
        try:
            # Create shareable link
            shareable_link = f"http://localhost:3000/view-capsule/{capsule_id}"
            
            message = MIMEMultipart()
            message['From'] = EMAIL_CONFIG['email_address']
            message['To'] = ', '.join(recipient_emails)
            message['Subject'] = f'🎉 Your Time Capsule "{capsule_title}" is Ready!'
            
            # Create email body with shareable link
            body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #696FC7, #A7AAE1); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .capsule-info {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #696FC7; }}
                    .button {{ display: inline-block; background: #696FC7; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-size: 16px; font-weight: bold; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎁 Your Time Capsule is Ready!</h1>
                    </div>
                    <div class="content">
                        <h2>Hello! 👋</h2>
                        
                        <div class="capsule-info">
                            <h3>📦 You've Received a Time Capsule!</h3>
                            <p><strong>From:</strong> {sender_name}</p>
                            <p><strong>Title:</strong> {capsule_title}</p>
                            <p><strong>Scheduled for:</strong> {delivery_date}</p>
                        </div>
                        
                        <p>{sender_name} sent you this time capsule from the past! ✨</p>
                        
                        <div style="text-align: center;">
                            <a href="{shareable_link}" class="button">🎁 Open Your Time Capsule</a>
                        </div>
                        
                        <p><em>Or copy this link: {shareable_link}</em></p>
                        
                        <p>This link will allow you to view the capsule directly without logging in!</p>
                    </div>
                    <div class="footer">
                        <p>Sent with 💌 from Time Capsule App</p>
                        <p>This is an automated message, please do not reply.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            message.attach(MIMEText(body, 'html'))
            
            # Send email
            print(f"📧 Sending email to: {recipient_emails}")
            print(f"🔗 Shareable link: {shareable_link}")
            
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()
            server.login(EMAIL_CONFIG['email_address'], EMAIL_CONFIG['email_password'])
            server.send_message(message)
            server.quit()
            
            print(f"✅ Email successfully sent to: {recipient_emails}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            # Enhanced fallback with shareable link
            shareable_link = f"http://localhost:3000/view-capsule/{capsule_id}"
            print("=" * 70)
            print("📧 EMAIL NOTIFICATION DETAILS (Email failed to send)")
            print("=" * 70)
            print(f"TO: {', '.join(recipient_emails)}")
            print(f"SUBJECT: 🎉 Your Time Capsule '{capsule_title}' is Ready!")
            print(f"FROM: {sender_name}")
            print(f"SHAREABLE LINK: {shareable_link}")
            print(f"CAPSULE TITLE: {capsule_title}")
            print(f"DELIVERY DATE: {delivery_date}")
            print("=" * 70)
            return False

class CapsuleScheduler:
    def __init__(self, capsule_storage, user_storage):
        self.capsule_storage = capsule_storage
        self.user_storage = user_storage
    
    def check_due_capsules(self):
        """Check for capsules that are due and send REAL notifications"""
        all_capsules = self.capsule_storage.get_all_capsules()
        
        today = datetime.now().date()
        print(f"🔍 Checking for due capsules... ({len(all_capsules)} total capsules)")
        
        for capsule in all_capsules:
            if capsule.get('status') == 'locked':
                try:
                    delivery_date = datetime.fromisoformat(capsule['delivery_date']).date()
                    if delivery_date <= today:
                        print(f"🎯 Capsule '{capsule['title']}' is due! Sending notifications...")
                        
                        # Mark as ready
                        self.capsule_storage.update_capsule(capsule['id'], {'status': 'ready'})
                        
                        # Get sender info
                        sender = self.user_storage.get_user_by_id(capsule['user_id'])
                        sender_name = sender['name'] if sender else 'A Friend'
                        
                        # Prepare recipient emails
                        recipient_emails = []
                        
                        # Add sender for notification (so they know it was delivered)
                        if sender:
                            recipient_emails.append(sender['email'])
                            print(f"👤 Added sender: {sender['email']}")
                        
                        # Add other recipients if any
                        if capsule.get('recipient_type') == 'multiple' and 'recipients' in capsule:
                            recipient_emails.extend(capsule['recipients'])
                            print(f"👥 Added multiple recipients: {capsule['recipients']}")
                        elif capsule.get('recipient_type') == 'other' and 'recipient_email' in capsule:
                            recipient_emails.append(capsule['recipient_email'])
                            print(f"👤 Added recipient: {capsule['recipient_email']}")
                        
                        # Remove duplicates
                        recipient_emails = list(set(recipient_emails))
                        
                        # Send REAL email notification with sender name
                        if recipient_emails:
                            EmailService.send_capsule_notification(
                                recipient_emails,
                                capsule['title'],
                                capsule['delivery_date'],
                                capsule['id'],
                                sender_name
                            )
                        else:
                            print("ℹ️  No recipients. Showing notification details:")
                            print(f"   Capsule: {capsule['title']}")
                            print(f"   From: {sender_name}")
                            print(f"   Recipients: {recipient_emails}")
                            print(f"   Delivery Date: {capsule['delivery_date']}")
                            
                except Exception as e:
                    print(f"❌ Error processing capsule {capsule.get('id')}: {e}")

# Initialize storage
user_storage = UserStorage()
capsule_storage = CapsuleStorage()
scheduler = CapsuleScheduler(capsule_storage, user_storage)

# Auth Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        user_data = request.json
        required_fields = ['email', 'password', 'name']
        
        for field in required_fields:
            if field not in user_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        if user_storage.get_user_by_email(user_data['email']):
            return jsonify({'error': 'User already exists'}), 400
        
        user_id = user_storage.create_user(user_data)
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'user': {
                'id': user_id,
                'email': user_data['email'],
                'name': user_data['name']
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        credentials = request.json
        if not credentials or 'email' not in credentials or 'password' not in credentials:
            return jsonify({'error': 'Email and password required'}), 400
        
        user = user_storage.get_user_by_email(credentials['email'])
        if not user or not check_password_hash(user['password'], credentials['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=user['id'])
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'name': user['name']
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = user_storage.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'created_at': user['created_at']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Profile Routes
@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    """Get current user's profile"""
    try:
        user_id = get_jwt_identity()
        user = user_storage.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Remove sensitive data
        user.pop('password', None)
        return jsonify(user)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    """Update current user's profile"""
    try:
        user_id = get_jwt_identity()
        updates = request.json
        
        # Validate email if being updated
        if 'email' in updates:
            if user_storage.get_user_by_email(updates['email']):
                # Check if it's the current user's email
                current_user = user_storage.get_user_by_id(user_id)
                if current_user['email'] != updates['email']:
                    return jsonify({'error': 'Email already in use'}), 400
        
        # Validate password if being updated
        if 'password' in updates and updates['password']:
            if len(updates['password']) < 6:
                return jsonify({'error': 'Password must be at least 6 characters'}), 400
            if 'current_password' not in updates:
                return jsonify({'error': 'Current password required to change password'}), 400
            
            # Verify current password
            current_user = user_storage.get_user_by_id(user_id)
            if not check_password_hash(current_user['password'], updates['current_password']):
                return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Update user
        updated_user = user_storage.update_user(user_id, updates)
        if not updated_user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': updated_user
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """Get user statistics"""
    try:
        user_id = get_jwt_identity()
        user = user_storage.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get sent capsules
        sent_capsules = capsule_storage.get_user_capsules(user_id)
        
        # Get received capsules
        received_capsules = capsule_storage.get_received_capsules(user['email'])
        
        # Calculate statistics
        total_sent = len(sent_capsules)
        total_received = len(received_capsules)
        
        # Count by status
        locked_sent = len([c for c in sent_capsules if c.get('status') == 'locked'])
        ready_sent = len([c for c in sent_capsules if c.get('status') == 'ready'])
        
        # Count by category
        categories = {}
        for capsule in sent_capsules:
            category = capsule.get('category', 'other')
            categories[category] = categories.get(category, 0) + 1
        
        stats = {
            'total_sent': total_sent,
            'total_received': total_received,
            'total_capsules': total_sent + total_received,
            'locked_sent': locked_sent,
            'ready_sent': ready_sent,
            'categories': categories,
            'joined_date': user['created_at'],
            'days_since_join': (datetime.now() - datetime.fromisoformat(user['created_at'])).days
        }
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Enhanced Capsule Routes
@app.route('/api/capsules', methods=['GET'])
@jwt_required()
def get_capsules():
    """Get all capsules for current user (sent by them)"""
    try:
        user_id = get_jwt_identity()
        query = request.args.get('q')
        category = request.args.get('category')
        tags = request.args.getlist('tags')
        status = request.args.get('status')
        
        if any([query, category, tags, status]):
            capsules = capsule_storage.search_capsules(user_id, query, category, tags, status)
        else:
            capsules = capsule_storage.get_user_capsules(user_id)
        
        return jsonify(capsules)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/capsules/sent', methods=['GET'])
@jwt_required()
def get_sent_capsules():
    """Get capsules sent by current user"""
    try:
        user_id = get_jwt_identity()
        capsules = capsule_storage.get_user_capsules(user_id)
        return jsonify(capsules)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/capsules/received', methods=['GET'])
@jwt_required()
def get_received_capsules():
    """Get capsules where current user is a recipient"""
    try:
        user_id = get_jwt_identity()
        user = user_storage.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        received_capsules = capsule_storage.get_received_capsules(user['email'])
        return jsonify(received_capsules)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/capsules', methods=['POST'])
@jwt_required()
def create_capsule():
    try:
        user_id = get_jwt_identity()
        capsule_data = request.json
        capsule_data['user_id'] = user_id
        
        required_fields = ['title', 'message', 'delivery_date', 'recipient_type']
        for field in required_fields:
            if field not in capsule_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Handle multiple recipients
        if capsule_data['recipient_type'] == 'multiple' and 'recipients' not in capsule_data:
            return jsonify({'error': 'Missing recipients for multiple recipients'}), 400
        
        capsule_id = capsule_storage.save_capsule(capsule_data)
        return jsonify({'id': capsule_id, 'message': 'Capsule created successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/capsules/<capsule_id>', methods=['GET'])
@jwt_required()
def get_capsule(capsule_id):
    try:
        user_id = get_jwt_identity()
        capsule = capsule_storage.get_capsule(capsule_id)
        
        if not capsule or capsule.get('user_id') != user_id:
            return jsonify({'error': 'Capsule not found'}), 404
        
        return jsonify(capsule)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/capsules/shared/<capsule_id>', methods=['GET'])
def get_shared_capsule(capsule_id):
    """Public endpoint to view shared capsules (no auth required)"""
    try:
        capsule = capsule_storage.get_capsule(capsule_id)
        
        if not capsule:
            return jsonify({'error': 'Capsule not found'}), 404
        
        # Only return capsule if it's ready to open
        if capsule.get('status') != 'ready':
            return jsonify({'error': 'Capsule is not ready yet'}), 403
        
        # Get sender info
        sender = user_storage.get_user_by_id(capsule['user_id'])
        sender_name = sender['name'] if sender else 'A Friend'
        
        # Return basic capsule info for sharing
        shared_capsule = {
            'id': capsule['id'],
            'title': capsule['title'],
            'message': capsule['message'],
            'delivery_date': capsule['delivery_date'],
            'created_at': capsule['created_at'],
            'sender_name': sender_name,
            'media_files': capsule.get('media_files', [])
        }
        
        return jsonify(shared_capsule)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/capsules/<capsule_id>', methods=['PUT'])
@jwt_required()
def update_capsule(capsule_id):
    try:
        user_id = get_jwt_identity()
        capsule = capsule_storage.get_capsule(capsule_id)
        
        if not capsule or capsule.get('user_id') != user_id:
            return jsonify({'error': 'Capsule not found'}), 404
        
        updates = request.json
        updated_capsule = capsule_storage.update_capsule(capsule_id, updates)
        
        return jsonify(updated_capsule)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/capsules/<capsule_id>', methods=['DELETE'])
@jwt_required()
def delete_capsule(capsule_id):
    try:
        user_id = get_jwt_identity()
        capsule = capsule_storage.get_capsule(capsule_id)
        
        if not capsule or capsule.get('user_id') != user_id:
            return jsonify({'error': 'Capsule not found'}), 404
        
        success = capsule_storage.delete_capsule(capsule_id)
        if success:
            return jsonify({'message': 'Capsule deleted successfully'})
        return jsonify({'error': 'Capsule not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/capsules/categories', methods=['GET'])
@jwt_required()
def get_categories():
    categories = ['personal', 'birthday', 'anniversary', 'graduation', 'travel', 'goals', 'other']
    return jsonify(categories)

@app.route('/api/media/<filename>')
def get_media(filename):
    """Serve media files (public for shared capsules)"""
    try:
        filepath = capsule_storage.get_media_file(filename)
        if filepath:
            return send_file(filepath)
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# Background scheduler thread
def run_scheduler():
    """Background thread to check for due capsules"""
    while True:
        try:
            scheduler.check_due_capsules()
        except Exception as e:
            print(f"Scheduler error: {e}")
        threading.Event().wait(60)  # Check every minute for demo

# Start scheduler when app starts
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Enhanced Time Capsule Backend Started!")
    print("=" * 60)
    print("📧 Features:")
    print("  • User Authentication (Login/Register)")
    print("  • REAL Email Notifications with Shareable Links")
    print("  • Separate Sent & Received Capsules")
    print("  • Public Capsule Viewing (No Login Required)")
    print("  • Search and Category Filtering")
    print("  • Multiple Recipients Support")
    print("  • Profile Management with Statistics")
    print("=" * 60)
    print("📍 API: http://localhost:5000")
    print("🔑 JWT Authentication: Enabled")
    
    # Check email configuration
    if EMAIL_CONFIG['email_password']:
        print("✅ Email: CONFIGURED - Real emails will be sent")
        print(f"   Using: {EMAIL_CONFIG['email_address']}")
    else:
        print("⚠️  Email: NOT CONFIGURED - Set EMAIL_PASSWORD to enable real emails")
        print("   Currently showing notifications in console only")
    
    print("🔔 Capsule Scheduler: Running (checks every minute)")
    print("=" * 60)
    
    app.run(debug=True, port=5000)