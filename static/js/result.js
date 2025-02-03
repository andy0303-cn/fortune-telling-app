document.addEventListener('DOMContentLoaded', function() {
    try {
        // 从 localStorage 获取数据
        const rawData = localStorage.getItem('fortuneResult');
        console.log('Raw data from localStorage:', rawData);
        
        if (!rawData) {
            throw new Error('No data found in localStorage');
        }

        // 解析 JSON 字符串
        const fortuneResult = JSON.parse(rawData);
        console.log('Parsed fortune result:', fortuneResult);

        // 填充基本信息
        const params = new URLSearchParams(window.location.search);
        document.getElementById('userName').textContent = params.get('name') || '未知';
        document.getElementById('userGender').textContent = params.get('gender') === 'F' ? '女' : '男';
        document.getElementById('userBirthdate').textContent = params.get('birthdate') || '未知';
        document.getElementById('userBirthplace').textContent = params.get('birthplace') || '未知';

        // 填充命理信息
        if (fortuneResult.basic_info) {
            const basicInfo = fortuneResult.basic_info;
            document.getElementById('userZodiac').textContent = basicInfo.zodiac || '未知';
            document.getElementById('userWesternSign').textContent = basicInfo.western_sign || '未知';
            document.getElementById('userBazi').textContent = basicInfo.bazi ? basicInfo.bazi.full : '未知';
            document.getElementById('userWuxing').textContent = basicInfo.wuxing ? basicInfo.wuxing.dominant : '未知';
        }

        // 填充分析内容
        const sections = {
            'overall': '整体运势',
            'career': '事业运势',
            'wealth': '财运分析',
            'love': '感情运势',
            'health': '健康提醒',
            'relationships': '人际关系'
        };

        Object.entries(sections).forEach(([key, title]) => {
            const data = fortuneResult[key];
            console.log(`Filling ${title}:`, data);
            if (data) {
                fillAnalysisSection(key, data);
            }
        });

    } catch (error) {
        console.error('Error processing fortune result:', error);
        alert('显示结果时出现错误，请重试');
    }
});

function fillAnalysisSection(sectionId, data) {
    const section = document.getElementById(sectionId);
    if (!section) return;

    // 填充摘要
    if (data.summary) {
        const summaryElem = section.querySelector('.summary');
        if (summaryElem) {
            summaryElem.textContent = data.summary;
        }
    }

    // 填充分析列表
    if (data.analysis) {
        const analysisList = section.querySelector('.analysis-list');
        if (analysisList) {
            analysisList.innerHTML = '';
            data.analysis.forEach(item => {
                const p = document.createElement('p');
                p.textContent = item;
                analysisList.appendChild(p);
            });
        }
    }

    // 填充建议列表
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

    // 填充年度运势
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

    // 填充月度趋势
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