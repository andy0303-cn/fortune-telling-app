document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('fortuneForm');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // 获取表单数据
        const formData = new FormData(form);
        const data = {
            name: formData.get('name'),
            gender: formData.get('gender'),
            birthdate: formData.get('birthdate'),
            birthplace: formData.get('birthplace')
        };
        
        try {
            // 发送请求
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
                    // 将数据添加到 URL 参数
                    const params = new URLSearchParams({
                        name: data.name,
                        gender: data.gender,
                        birthdate: data.birthdate,
                        birthplace: data.birthplace
                    });
                    // 跳转到结果页面
                    window.location.href = `/result?${params.toString()}`;
                } else {
                    throw new Error('分析失败');
                }
            } else {
                throw new Error('请求失败');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('发生错误，请重试');
        }
    });
}); 