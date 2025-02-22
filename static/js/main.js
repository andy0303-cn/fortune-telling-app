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
                    // 存储分析结果
                    localStorage.setItem('fortuneResult', JSON.stringify(result.data));
                    
                    // 构建查询参数
                    const params = new URLSearchParams({
                        name: data.name,
                        gender: data.gender === 'M' ? '男' : '女',
                        birthdate: new Date(data.birthdate).toLocaleString('zh-CN'),
                        birthplace: data.birthplace
                    }).toString();
                    
                    // 使用相对路径进行跳转
                    window.location.replace(`/result?${params}`);
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