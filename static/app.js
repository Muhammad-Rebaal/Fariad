document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('geminiForm');
    const imageInput = document.getElementById('imageInput');
    const filePreview = document.getElementById('filePreview');
    const fileNameDisplay = document.getElementById('fileName');
    const removeFileBtn = document.getElementById('removeFileBtn');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const responseSection = document.getElementById('responseSection');
    const responseContent = document.getElementById('responseContent');
    const badge = responseSection.querySelector('.badge');
    const fileUploadLabel = document.querySelector('.file-upload-label');

    // Handle drag and drop styling
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileUploadLabel.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        fileUploadLabel.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        fileUploadLabel.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        fileUploadLabel.style.borderColor = 'var(--primary)';
        fileUploadLabel.style.background = 'rgba(99, 102, 241, 0.1)';
    }

    function unhighlight(e) {
        fileUploadLabel.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        fileUploadLabel.style.background = 'rgba(15, 23, 42, 0.3)';
    }

    fileUploadLabel.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        let dt = e.dataTransfer;
        let files = dt.files;
        imageInput.files = files;
        updateFilePreview();
    }

    // Handle file selection
    imageInput.addEventListener('change', updateFilePreview);

    function updateFilePreview() {
        if (imageInput.files.length > 0) {
            const file = imageInput.files[0];
            fileNameDisplay.textContent = file.name;
            filePreview.classList.remove('hidden');
            fileUploadLabel.style.display = 'none';
        } else {
            resetFilePreview();
        }
    }

    removeFileBtn.addEventListener('click', (e) => {
        e.preventDefault();
        imageInput.value = '';
        resetFilePreview();
    });

    function resetFilePreview() {
        fileNameDisplay.textContent = 'No file chosen';
        filePreview.classList.add('hidden');
        fileUploadLabel.style.display = 'flex';
    }

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // UI updates for loading state
        submitBtn.disabled = true;
        btnText.textContent = 'Processing...';
        spinner.classList.remove('hidden');
        loadingOverlay.classList.add('active');
        responseSection.classList.add('hidden');
        
        const formData = new FormData(form);
        
        // Auto-detect backend URL: Use the provided DevTunnels URL when deployed to Vercel, 
        // otherwise use current origin if we are running locally.
        const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        const apiUrl = isLocalhost ? window.location.origin : 'https://7qgj0h26-8000.inc1.devtunnels.ms';
        const baseUrl = apiUrl.endsWith('/') ? apiUrl.slice(0, -1) : apiUrl;
        
        try {
            const response = await fetch(`${baseUrl}/ask`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            // Re-enable UI
            submitBtn.disabled = false;
            btnText.textContent = 'Automate Request';
            spinner.classList.add('hidden');
            loadingOverlay.classList.remove('active');
            
            // Display results
            responseSection.classList.remove('hidden');
            
            if (response.ok && data.status === 'success') {
                badge.textContent = 'Success';
                badge.className = 'badge';
                responseContent.textContent = data.response;
                // Scroll to response
                responseSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                throw new Error(data.message || 'Unknown error occurred');
            }
            
        } catch (error) {
            // Re-enable UI
            submitBtn.disabled = false;
            btnText.textContent = 'Automate Request';
            spinner.classList.add('hidden');
            loadingOverlay.classList.remove('active');
            
            // Show error
            responseSection.classList.remove('hidden');
            badge.textContent = 'Error';
            badge.className = 'badge error';
            responseContent.textContent = error.message;
        }
    });
});
