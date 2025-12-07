import React, { useState } from 'react';

const CapsuleForm = ({ onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    message: '',
    delivery_date: '',
    recipient_type: 'self',
    recipient_email: '',
    media_files: []
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files);
    const fileReaders = files.map(file => {
      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          resolve({
            filename: file.name,
            content: e.target.result,
            type: file.type
          });
        };
        reader.readAsDataURL(file);
      });
    });

    Promise.all(fileReaders).then(fileData => {
      setFormData(prev => ({
        ...prev,
        media_files: [...prev.media_files, ...fileData]
      }));
    });
  };

  const removeFile = (index) => {
    setFormData(prev => ({
      ...prev,
      media_files: prev.media_files.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="capsule-form-container">
      <div className="card">
        <div className="card-header">
          <i className="fas fa-plus-circle"></i> Create New Time Capsule
        </div>
        <div className="card-body">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="title">Capsule Title *</label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="message">Your Message *</label>
              <textarea
                id="message"
                name="message"
                value={formData.message}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Add Photos or Videos</label>
              <div className="upload-area">
                <input
                  type="file"
                  multiple
                  accept="image/*,video/*"
                  onChange={handleFileUpload}
                />
                <i className="fas fa-cloud-upload-alt"></i>
                <p>Click to upload or drag and drop</p>
                <p className="small">PNG, JPG, MP4 up to 10MB</p>
              </div>
              <div className="media-preview">
                {formData.media_files.map((file, index) => (
                  <div key={index} className="media-item">
                    {file.type.startsWith('image/') ? (
                      <img src={file.content} alt="Preview" />
                    ) : (
                      <video controls>
                        <source src={file.content} type={file.type} />
                      </video>
                    )}
                    <button
                      type="button"
                      className="remove"
                      onClick={() => removeFile(index)}
                    >
                      <i className="fas fa-times"></i>
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="delivery_date">Delivery Date *</label>
              <input
                type="date"
                id="delivery_date"
                name="delivery_date"
                value={formData.delivery_date}
                onChange={handleInputChange}
                min={new Date().toISOString().split('T')[0]}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="recipient_type">Send To *</label>
              <select
                id="recipient_type"
                name="recipient_type"
                value={formData.recipient_type}
                onChange={handleInputChange}
              >
                <option value="self">Myself</option>
                <option value="other">Someone Else</option>
              </select>
            </div>

            {formData.recipient_type === 'other' && (
              <div className="form-group">
                <label htmlFor="recipient_email">Recipient's Email *</label>
                <input
                  type="email"
                  id="recipient_email"
                  name="recipient_email"
                  value={formData.recipient_email}
                  onChange={handleInputChange}
                  required
                />
              </div>
            )}

            <div className="form-actions">
              <button type="button" className="btn btn-secondary" onClick={onCancel}>
                Cancel
              </button>
              <button type="submit" className="btn btn-primary">
                <i className="fas fa-lock"></i> Lock Time Capsule
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default CapsuleForm;