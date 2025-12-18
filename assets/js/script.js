const form = document.getElementById('convertForm');
const imageInput = document.getElementById('imageInput');
const columnsInput = document.getElementById('columns');
const contrastInput = document.getElementById('contrast');
const output = document.getElementById('output');
const statusEl = document.getElementById('status');
const outputSection = document.getElementById('outputSection');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const downloadPngBtn = document.getElementById('downloadPngBtn');
const convertBtn = document.getElementById('convertBtn');

let asciiText = '';

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!imageInput.files || imageInput.files.length === 0) {
        statusEl.textContent = '⚠️ Please select an image';
        statusEl.className = 'status error';
        return;
    }
    
    // Show loading state
    convertBtn.disabled = true;
    convertBtn.textContent = 'Converting...';
    statusEl.textContent = '🔄 Processing image...';
    statusEl.className = 'status loading';
    outputSection.style.display = 'none';
    
    const formData = new FormData();
    formData.append('image', imageInput.files[0]);
    formData.append('columns', columnsInput.value);
    formData.append('contrast', contrastInput.value);
    formData.append('monochrome', document.querySelector('input[name="monochrome"]:checked').value);
    
    try {
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Conversion failed');
        }
        
        asciiText = data.ascii;
        htmlContent = data.html;
        output.innerHTML = htmlContent;
        
        const lines = asciiText.split('\n').length;
        statusEl.textContent = `✅ Converted! ${lines} lines`;
        statusEl.className = 'status success';
        outputSection.style.display = 'block';
        
    } catch (error) {
        statusEl.textContent = `❌ Error: ${error.message}`;
        statusEl.className = 'status error';
    } finally {
        convertBtn.disabled = false;
        convertBtn.textContent = 'Convert to ASCII';
    }
});

copyBtn.addEventListener('click', async () => {
    try {
        await navigator.clipboard.writeText(asciiText);
        statusEl.textContent = '✅ Copied to clipboard!';
        statusEl.className = 'status success';
    } catch (error) {
        statusEl.textContent = '❌ Failed to copy';
        statusEl.className = 'status error';
    }
});

downloadBtn.addEventListener('click', () => {
    const blob = new Blob([asciiText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ascii-art.txt';
    a.click();
    URL.revokeObjectURL(url);
    
    statusEl.textContent = '✅ Downloaded as TXT!';
    statusEl.className = 'status success';
});

downloadPngBtn.addEventListener('click', async () => {
    // Trigger download from server-generated PNG
    try {
        const formData = new FormData();
        formData.append('image', imageInput.files[0]);
        formData.append('columns', columnsInput.value);
        formData.append('contrast', contrastInput.value);
        formData.append('monochrome', document.querySelector('input[name="monochrome"]:checked').value);

        const response = await fetch('/download', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to generate PNG');
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'ascii_image.png';
        a.click();
        URL.revokeObjectURL(url);
        
        statusEl.textContent = '✅ Downloaded as PNG! Image saved successfully.';
        statusEl.className = 'status success';
    } catch (error) {
        statusEl.textContent = `❌ Error: ${error.message}`;
        statusEl.className = 'status error';
    }
});
