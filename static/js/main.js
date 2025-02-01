document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('fortune-form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('name').value,
            gender: document.querySelector('input[name="gender"]:checked').value,
            birthDate: document.getElementById('birthdate').value,
            birthPlace: document.getElementById('birthplace').value
        };
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                // 重定向到结果页面
                const params = new URLSearchParams({
                    name: formData.name,
                    gender: formData.gender,
                    birthdate: formData.birthDate,
                    birthplace: formData.birthPlace
                });
                window.location.href = `/result?${params.toString()}`;
            } else {
                alert('分析失败：' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('请求失败，请稍后重试');
        }
    });
});

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const form = document.getElementById('fortuneForm');
    form.insertBefore(errorDiv, form.firstChild);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 3000);
}

function submitForm() {
    // 添加加载状态
    document.getElementById('submit-btn').disabled = true;
    document.getElementById('submit-btn').textContent = '分析中...';
    
    // ... 现有代码 ...
} 