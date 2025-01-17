// Global variables
let generatedImageUrl = null;

// Utility functions
function showElement(element) {
    if (!element) return;
    element.style.display = 'block';
    element.classList.add('fade-in');
}

function hideElement(element) {
    if (!element) return;
    element.style.display = 'none';
    element.classList.remove('fade-in');
}

// Image generation function
async function generateImage(event) {
    event.preventDefault();
    
    const form = document.getElementById('festiveForm');
    const prompt = document.getElementById('prompt').value;
    const style = document.getElementById('style').value;
    const size = document.getElementById('size').value;
    const quality = document.getElementById('quality').value;
    const greeting = document.getElementById('greeting').value;
    const logoFile = document.getElementById('userLogo').files[0];

    if (!prompt) {
        alert('Please describe what you want in your festive image');
        return;
    }

    // Hide the create button
    const actionSection = document.querySelector('.action-section');
    hideElement(actionSection);

    // Show progress bar and loading animation
    const progressContainer = document.getElementById('progressContainer');
    const loading = document.getElementById('loading');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    
    showElement(progressContainer);
    showElement(loading);
    
    // Simulate progress updates
    let progress = 0;
    const progressInterval = setInterval(() => {
        if (progress < 90) {
            progress += Math.random() * 10;
            progress = Math.min(progress, 90);
            progressBar.style.width = `${progress}%`;
            
            // Update progress text
            if (progress < 30) {
                progressText.textContent = "Analyzing your request...";
            } else if (progress < 60) {
                progressText.textContent = "AI is creating your image...";
            } else {
                progressText.textContent = "Almost there...";
            }
        }
    }, 500);

    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('prompt', prompt);
        formData.append('style', style);
        formData.append('size', size);
        formData.append('quality', quality);
        if (greeting) formData.append('greeting', greeting);
        if (logoFile) formData.append('logo', logoFile);

        // Send API request
        const response = await fetch('/api/generate-festive-image/', {
            method: 'POST',
            body: formData
        });

        clearInterval(progressInterval);

        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                // Update progress to 100%
                progressBar.style.width = '100%';
                progressText.textContent = "Creation complete!";
                
                // Show generated image
                generatedImageUrl = data.image_url;
                const resultImage = document.getElementById('resultImage');
                resultImage.src = generatedImageUrl;
                showElement(resultImage);
                
                // Show share options
                showElement(document.getElementById('shareOptions'));
                
                // Hide loading animation
                hideElement(loading);
                
                // Hide progress bar after 3 seconds
                setTimeout(() => {
                    hideElement(progressContainer);
                    // Show the create button again
                    showElement(actionSection);
                }, 3000);
            } else {
                throw new Error(data.error || 'Failed to generate image');
            }
        } else {
            throw new Error('Server response error');
        }
    } catch (error) {
        console.error('Error:', error);
        clearInterval(progressInterval);
        progressText.textContent = "Generation failed, please try again";
        progressBar.style.backgroundColor = "#ff4444";
        hideElement(loading);
        // Show the create button again on error
        showElement(actionSection);
        alert('Error generating image, please try again');
    }
}

// Logo preview functionality
document.getElementById('userLogo').addEventListener('change', function(e) {
    const preview = document.getElementById('logoPreview');
    const file = e.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            showElement(preview);
        }
        reader.readAsDataURL(file);
    }
});

// Greeting preview
document.getElementById('greeting').addEventListener('input', function(e) {
    const preview = document.getElementById('greetingPreview');
    preview.textContent = e.target.value;
});

// File drag and drop functionality
const uploadArea = document.querySelector('.upload-area');

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        document.getElementById('userLogo').files = e.dataTransfer.files;
        const event = new Event('change');
        document.getElementById('userLogo').dispatchEvent(event);
    }
});

// Share functionality
function showShareModal() {
    const modal = document.getElementById('shareModal');
    showElement(modal);
}

function closeShareModal() {
    const modal = document.getElementById('shareModal');
    hideElement(modal);
}

function downloadImage() {
    if (generatedImageUrl) {
        const link = document.createElement('a');
        link.href = generatedImageUrl;
        link.download = 'festive-image.png';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

async function shareToWeChat() {
    // WeChat sharing implementation
    alert('WeChat sharing coming soon');
}

async function shareToWeibo() {
    // Weibo sharing implementation
    const shareUrl = encodeURIComponent(window.location.href);
    const title = encodeURIComponent('Check out this festive image I created with AI!');
    window.open(`http://service.weibo.com/share/share.php?url=${shareUrl}&title=${title}`);
}

async function shareViaEmail() {
    const email = prompt('Enter recipient email address:');
    if (email) {
        try {
            const response = await fetch('/api/send-festive-email/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    image_url: generatedImageUrl
                })
            });
            
            const data = await response.json();
            if (data.success) {
                alert('Email sent successfully!');
            } else {
                throw new Error(data.error || 'Failed to send');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to send email, please try again');
        }
    }
}

// Modal close event
window.onclick = function(event) {
    const modal = document.getElementById('shareModal');
    if (event.target == modal) {
        hideElement(modal);
    }
}
