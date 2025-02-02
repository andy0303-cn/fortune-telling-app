document.addEventListener('DOMContentLoaded', function() {
    // 从 URL 获取用户信息
    const params = new URLSearchParams(window.location.search);
    
    // 获取分析结果
    const fortuneResult = JSON.parse(localStorage.getItem('fortuneResult') || '{}');
    
    // 填充基本信息
    document.getElementById('userName').textContent = params.get('name') || '未知';
    document.getElementById('userGender').textContent = params.get('gender') || '未知';
    document.getElementById('userBirthdate').textContent = params.get('birthdate') || '未知';
    document.getElementById('userBirthplace').textContent = params.get('birthplace') || '未知';
    
    if (fortuneResult.basic_info) {
        document.getElementById('userZodiac').textContent = fortuneResult.basic_info.zodiac || '未知';
        document.getElementById('userWesternSign').textContent = fortuneResult.basic_info.western_sign || '未知';
    }
    
    // 填充整体运势
    if (fortuneResult.overall) {
        const overallCard = document.getElementById('overall');
        overallCard.querySelector('.summary').textContent = fortuneResult.overall.summary;
        
        const analysisList = overallCard.querySelector('.analysis-list');
        fortuneResult.overall.analysis.forEach(item => {
            const p = document.createElement('p');
            p.textContent = item;
            analysisList.appendChild(p);
        });
        
        const highlightsList = overallCard.querySelector('.highlights-list');
        fortuneResult.overall.highlights.forEach(item => {
            const p = document.createElement('p');
            p.textContent = item;
            highlightsList.appendChild(p);
        });
    }
    
    // 填充事业运势
    if (fortuneResult.career) {
        const careerCard = document.getElementById('career');
        careerCard.querySelector('.summary').textContent = fortuneResult.career.summary;
        
        const analysisList = careerCard.querySelector('.analysis-list');
        fortuneResult.career.analysis.forEach(item => {
            const p = document.createElement('p');
            p.textContent = item;
            analysisList.appendChild(p);
        });
        
        const suggestionsList = careerCard.querySelector('.suggestions-list');
        fortuneResult.career.suggestions.forEach(item => {
            const p = document.createElement('p');
            p.textContent = item;
            suggestionsList.appendChild(p);
        });
    }
}); 