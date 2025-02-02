document.addEventListener('DOMContentLoaded', function() {
    // 从 URL 获取用户信息
    const params = new URLSearchParams(window.location.search);
    
    // 填充用户信息
    document.getElementById('userName').textContent = params.get('name') || '未知';
    document.getElementById('userGender').textContent = params.get('gender') || '未知';
    document.getElementById('userBirthdate').textContent = params.get('birthdate') || '未知';
    document.getElementById('userBirthplace').textContent = params.get('birthplace') || '未知';
    
    // 从 localStorage 获取分析结果
    const fortuneResult = JSON.parse(localStorage.getItem('fortuneResult') || '{}');
    
    // 填充分析结果
    document.querySelector('#overall p').textContent = fortuneResult.overall || '';
    document.querySelector('#career p').textContent = fortuneResult.career || '';
    document.querySelector('#wealth p').textContent = fortuneResult.wealth || '';
    document.querySelector('#love p').textContent = fortuneResult.love || '';
    document.querySelector('#health p').textContent = fortuneResult.health || '';
    document.querySelector('#relationships p').textContent = fortuneResult.relationships || '';
}); 