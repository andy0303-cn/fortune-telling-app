document.addEventListener('DOMContentLoaded', function() {
    // 从 URL 获取用户信息
    const params = new URLSearchParams(window.location.search);
    
    // 获取分析结果
    const fortuneResult = JSON.parse(localStorage.getItem('fortuneResult') || '{}');
    console.log('Loaded fortune result:', fortuneResult);  // 添加调试信息
    
    // 填充基本信息
    document.getElementById('userName').textContent = params.get('name') || '未知';
    document.getElementById('userGender').textContent = params.get('gender') === 'M' ? '男' : '女';
    document.getElementById('userBirthdate').textContent = params.get('birthdate') || '未知';
    document.getElementById('userBirthplace').textContent = params.get('birthplace') || '未知';
    
    if (fortuneResult.data && fortuneResult.data.basic_info) {
        const basicInfo = fortuneResult.data.basic_info;
        document.getElementById('userZodiac').textContent = basicInfo.zodiac || '未知';
        document.getElementById('userWesternSign').textContent = basicInfo.western_sign || '未知';
        document.getElementById('userBazi').textContent = basicInfo.bazi.full || '未知';
        document.getElementById('userWuxing').textContent = basicInfo.wuxing.dominant || '未知';
    }

    // 通用函数：填充分析内容
    function fillAnalysisSection(sectionId, data) {
        if (!data) {
            console.log(`No data for section: ${sectionId}`);  // 添加调试信息
            return;
        }
        console.log(`Filling section ${sectionId} with data:`, data);  // 添加调试信息
        
        const section = document.getElementById(sectionId);
        if (!section) {
            console.log(`Section element not found: ${sectionId}`);  // 添加调试信息
            return;
        }

        if (data.summary) {
            const summaryElem = section.querySelector('.summary');
            if (summaryElem) {
                summaryElem.textContent = data.summary;
            }
        }
        
        if (data.analysis) {
            const analysisList = section.querySelector('.analysis-list');
            analysisList.innerHTML = '';
            data.analysis.forEach(item => {
                const p = document.createElement('p');
                p.textContent = item;
                analysisList.appendChild(p);
            });
        }
        
        if (data.suggestions) {
            const suggestionsList = section.querySelector('.suggestions-list');
            if (suggestionsList) {
                suggestionsList.innerHTML = '';
                data.suggestions.forEach(item => {
                    const p = document.createElement('p');
                    p.textContent = item;
                    suggestionsList.appendChild(p);
                });
            }
        }

        if (data.yearly_fortune) {
            const yearlyFortune = section.querySelector('.yearly-fortune');
            if (yearlyFortune) {
                yearlyFortune.innerHTML = '';
                data.yearly_fortune.forEach(item => {
                    const p = document.createElement('p');
                    p.textContent = item;
                    yearlyFortune.appendChild(p);
                });
            }
        }

        if (data.monthly_trends) {
            const monthlyTrends = section.querySelector('.monthly-trends');
            if (monthlyTrends) {
                monthlyTrends.innerHTML = '';
                data.monthly_trends.forEach(item => {
                    const p = document.createElement('p');
                    p.textContent = item;
                    monthlyTrends.appendChild(p);
                });
            }
        }
    }

    // 填充所有分析内容
    if (fortuneResult.data) {
        console.log('Filling all sections with data:', fortuneResult.data);  // 添加调试信息
        fillAnalysisSection('overall', fortuneResult.data.overall);
        fillAnalysisSection('career', fortuneResult.data.career);
        fillAnalysisSection('wealth', fortuneResult.data.wealth);
        fillAnalysisSection('love', fortuneResult.data.love);
        fillAnalysisSection('health', fortuneResult.data.health);
        fillAnalysisSection('relationships', fortuneResult.data.relationships);
    } else {
        console.log('No fortune data available');  // 添加调试信息
    }
}); 