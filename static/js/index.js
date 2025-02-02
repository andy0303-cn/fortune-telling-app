document.getElementById('fortuneForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        gender: document.getElementById('gender').value,
        birthdate: document.getElementById('birthdate').value,
        birthplace: document.getElementById('birthplace').value
    };

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        console.log('Server response:', result);  // 添加调试信息

        // 存储结果
        localStorage.setItem('fortuneResult', JSON.stringify(result));
        console.log('Stored in localStorage:', localStorage.getItem('fortuneResult'));  // 验证存储

        // 跳转到结果页面
        window.location.href = `/result?name=${encodeURIComponent(formData.name)}&gender=${encodeURIComponent(formData.gender)}&birthdate=${encodeURIComponent(formData.birthdate)}&birthplace=${encodeURIComponent(formData.birthplace)}`;
    } catch (error) {
        console.error('Error:', error);
        alert('分析过程中出现错误，请重试');
    }
}); 