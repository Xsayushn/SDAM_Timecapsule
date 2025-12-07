import json
import os
import uuid
from datetime import datetime
from pathlib import Path

class CapsuleStorage:
    def __init__(self, storage_dir="capsules", media_dir="media"):
        self.storage_dir = Path(storage_dir)
        self.media_dir = self.storage_dir / media_dir
        self.storage_dir.mkdir(exist_ok=True)
        self.media_dir.mkdir(exist_ok=True)
    
    def save_capsule(self, capsule_data):
        """Save a new time capsule"""
        capsule_id = str(uuid.uuid4())
        capsule_data['id'] = capsule_id
        capsule_data['created_at'] = datetime.now().isoformat()
        capsule_data['status'] = 'locked'
        
        # Handle file uploads - FIXED: Proper base64 handling
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
        
        # Save capsule metadata
        capsule_file = self.storage_dir / f"{capsule_id}.json"
        with open(capsule_file, 'w') as f:
            json.dump(capsule_data, f, indent=2)
        
        return capsule_id
    
    def save_media_file(self, file_data):
        """Save media file and return filename"""
        filename = f"{uuid.uuid4()}_{file_data['filename']}"
        filepath = self.media_dir / filename
        
        # Handle base64 encoded files
        if isinstance(file_data['content'], str) and file_data['content'].startswith('data:'):
            import base64
            header, encoded = file_data['content'].split(',', 1)
            file_content = base64.b64decode(encoded)
        else:
            file_content = file_data['content']
        
        with open(filepath, 'wb') as f:
            f.write(file_content)
        
        return filename
    
    def get_capsule(self, capsule_id):
        """Get a specific capsule"""
        capsule_file = self.storage_dir / f"{capsule_id}.json"
        if not capsule_file.exists():
            return None
        
        with open(capsule_file, 'r') as f:
            return json.load(f)
    
    def get_all_capsules(self):
        """Get all capsules"""
        capsules = []
        for file in self.storage_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    capsule_data = json.load(f)
                    capsules.append(capsule_data)
            except Exception as e:
                print(f"Error reading capsule file {file}: {e}")
        
        # Sort by delivery date
        capsules.sort(key=lambda x: x.get('delivery_date', ''))
        return capsules
    
    def delete_capsule(self, capsule_id):
        """Delete a capsule"""
        capsule_file = self.storage_dir / f"{capsule_id}.json"
        if capsule_file.exists():
            # Also delete associated media files
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
        """Get media file path"""
        filepath = self.media_dir / filename
        if filepath.exists():
            return filepath
        return None