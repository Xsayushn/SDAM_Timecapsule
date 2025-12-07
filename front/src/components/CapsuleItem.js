import React from 'react';

const CapsuleItem = ({ capsule, onDelete }) => {
  const calculateCountdown = (deliveryDate) => {
    const today = new Date();
    const delivery = new Date(deliveryDate);
    const diffTime = delivery - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays > 0) {
      return `${diffDays} day${diffDays !== 1 ? 's' : ''}`;
    } else if (diffDays === 0) {
      return 'Today!';
    } else {
      return 'Ready to open!';
    }
  };

  return (
    <div className="capsule-item">
      <div className="capsule-info">
        <h3>{capsule.title}</h3>
        <p className="capsule-message">{capsule.message}</p>
        
        {capsule.media_files && capsule.media_files.length > 0 && (
          <div className="capsule-media-preview">
            {capsule.media_files.slice(0, 3).map((file, index) => (
              <div key={index} className="media-thumbnail">
                {file.type.startsWith('image/') ? (
                  <img 
                    src={`http://localhost:5000/api/media/${file.filename}`} 
                    alt={file.original_name}
                  />
                ) : (
                  <div className="video-thumbnail">
                    <i className="fas fa-video"></i>
                  </div>
                )}
              </div>
            ))}
            {capsule.media_files.length > 3 && (
              <div className="media-count">+{capsule.media_files.length - 3} more</div>
            )}
          </div>
        )}
        
        <div className="capsule-meta">
          <span>
            <i className="fas fa-user"></i> 
            To: {capsule.recipient_type === 'self' ? 'Myself' : capsule.recipient_email}
          </span>
          <span>
            <i className="fas fa-calendar"></i> 
            Delivery: {new Date(capsule.delivery_date).toLocaleDateString()}
          </span>
          <span className="countdown">
            <i className="fas fa-clock"></i> 
            {calculateCountdown(capsule.delivery_date)}
          </span>
          <span>
            <i className="fas fa-calendar-plus"></i>
            Created: {new Date(capsule.created_at).toLocaleDateString()}
          </span>
        </div>
      </div>
      <div className="capsule-actions">
        <button 
          className="btn-danger"
          onClick={() => onDelete(capsule.id)}
          title="Delete capsule"
        >
          <i className="fas fa-trash"></i>
        </button>
      </div>
    </div>
  );
};

export default CapsuleItem;