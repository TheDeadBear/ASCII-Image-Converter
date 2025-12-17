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
        output.textContent = asciiText;
        
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

downloadPngBtn.addEventListener('click', () => {
    // Create canvas for ASCII art rendering
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // Configure font and get measurements
    const fontSize = 12;
    const fontFamily = 'Courier New, monospace';
    ctx.font = `${fontSize}px ${fontFamily}`;
    
    // Calculate canvas dimensions based on ASCII text
    const lines = asciiText.split('\n');
    const maxLineLength = Math.max(...lines.map(line => line.length));
    const charWidth = ctx.measureText('M').width; // Monospace character width
    const lineHeight = fontSize * 1.2; // Line spacing
    
    canvas.width = Math.ceil(maxLineLength * charWidth) + 40; // Add padding
    canvas.height = Math.ceil(lines.length * lineHeight) + 40; // Add padding
    
    // Fill background
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw ASCII text
    ctx.fillStyle = '#00ff00';
    ctx.font = `${fontSize}px ${fontFamily}`;
    ctx.textBaseline = 'top';
    
    lines.forEach((line, index) => {
        ctx.fillText(line, 20, 20 + (index * lineHeight));
    });
    
    // Convert canvas to blob and download
    canvas.toBlob((blob) => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'ascii-art.png';
        a.click();
        URL.revokeObjectURL(url);
        
        statusEl.textContent = '✅ Downloaded as PNG! Image saved successfully.';
        statusEl.className = 'status success';
    }, 'image/png');
});
