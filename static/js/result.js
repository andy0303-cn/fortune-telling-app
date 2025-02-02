document.addEventListener('DOMContentLoaded', function() {
    try {
        // 从 localStorage 获取数据
        const rawData = localStorage.getItem('fortuneResult');
        console.log('Raw data from localStorage:', rawData);
        
        if (!rawData) {
            throw new Error('No data found in localStorage');
        }

        const fortuneResult = JSON.parse(rawData);
        console.log('Parsed fortune result:', fortuneResult);

        if (!fortuneResult.data) {
            throw new Error('Invalid data structure: missing data property');
        }

        // 填充基本信息
        const basicInfo = fortuneResult.data.basic_info;
        if (basicInfo) {
            document.getElementById('userBazi').textContent = basicInfo.bazi ? basicInfo.bazi.full : '未知';
            document.getElementById('userWuxing').textContent = basicInfo.wuxing ? basicInfo.wuxing.dominant : '未知';
        }

        // 填充分析内容
        Object.entries({
            'overall': '整体运势',
            'career': '事业运势',
            'wealth': '财运分析',
            'love': '感情运势',
            'health': '健康提醒',
            'relationships': '人际关系'
        }).forEach(([key, title]) => {
            const data = fortuneResult.data[key];
            if (data) {
                console.log(`Filling ${title}:`, data);
                fillAnalysisSection(key, data);
            } else {
                console.warn(`Missing data for ${title}`);
            }
        });

    } catch (error) {
        console.error('Error processing fortune result:', error);
        alert('显示结果时出现错误，请重试');
    }
});

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