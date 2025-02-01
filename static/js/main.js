document.addEventListener('DOMContentLoaded', function() {
    const fortuneForm = document.getElementById('fortuneForm');
    const submitButton = fortuneForm.querySelector('button[type="submit"]');
    
    fortuneForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // 禁用提交按钮并显示加载状态
        submitButton.disabled = true;
        submitButton.textContent = '正在解读...';
        
        const formData = new FormData(fortuneForm);
        const birthDate = formData.get('birthdate');
        // 格式化日期
        const formattedDate = new Date(birthDate).toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });

        const data = {
            name: formData.get('name'),
            gender: formData.get('gender'),
            birthDate: formattedDate,
            birthPlace: formData.get('birthplace')
        };
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                const result = await response.json();
                if (result.status === 'success') {
                    // 将用户数据添加到 URL 参数
                    const params = new URLSearchParams({
                        name: data.name,
                        gender: data.gender,
                        birthdate: data.birthDate,
                        birthplace: data.birthPlace
                    });
                    window.location.href = `/result?${params.toString()}`;
                } else {
                    showError(result.message || '分析失败');
                    console.error('API Error:', result);
                }
            } else {
                const error = await response.json();
                showError(error.message || '提交失败，请重试');
                console.error('HTTP Error:', error);
            }
        } catch (error) {
            console.error('Network Error:', error);
            showError('发生错误，请重试');
        } finally {
            // 恢复提交按钮状态
            submitButton.disabled = false;
            submitButton.textContent = '开始解读';
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