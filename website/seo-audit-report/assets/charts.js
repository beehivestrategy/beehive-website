(function() {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim() || '#4ade80';
  var accent2 = style.getPropertyValue('--accent2').trim() || '#facc15';
  var ink = style.getPropertyValue('--ink').trim() || '#e8efe9';
  var muted = style.getPropertyValue('--muted').trim() || '#88998c';
  var rule = style.getPropertyValue('--rule').trim() || '#1e2a28';
  var bg2 = style.getPropertyValue('--bg2').trim() || '#111817';
  var fail = '#f87171';
  var warn = '#fb923c';
  var pass = '#4ade80';

  // --- Chart 1: Status Overview (horizontal bar) ---
  var chart1 = echarts.init(document.getElementById('chart-status'), null, { renderer: 'svg' });
  chart1.setOption({
    animation: false,
    tooltip: {
      appendToBody: true,
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: bg2,
      borderColor: rule,
      textStyle: { color: ink, fontSize: 13 }
    },
    grid: { left: 120, right: 40, top: 10, bottom: 20 },
    xAxis: {
      type: 'value',
      max: 14,
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { show: false },
      splitLine: { show: false }
    },
    yAxis: {
      type: 'category',
      data: ['OG Tags', 'JSON-LD', 'Image Alt Text', 'HTTPS', '404 Page', 'llms.txt', 'WP 410 Cleanup', 'Broken Links', 'Canonical Tags', 'Hreflang Tags', 'Meta Descriptions', 'Sitemap Coverage', 'Duplicate Descriptions', 'Title Tags'],
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: muted, fontSize: 12 }
    },
    series: [{
      type: 'bar',
      barWidth: 14,
      data: [
        { value: 10, itemStyle: { color: pass } },
        { value: 10, itemStyle: { color: pass } },
        { value: 10, itemStyle: { color: pass } },
        { value: 10, itemStyle: { color: pass } },
        { value: 10, itemStyle: { color: pass } },
        { value: 10, itemStyle: { color: pass } },
        { value: 10, itemStyle: { color: pass } },
        { value: 10, itemStyle: { color: pass } },
        { value: 10, itemStyle: { color: pass } },
        { value: 10, itemStyle: { color: pass } },
        { value: 7, itemStyle: { color: warn } },
        { value: 6, itemStyle: { color: warn } },
        { value: 4, itemStyle: { color: fail } },
        { value: 3, itemStyle: { color: fail } }
      ],
      label: {
        show: true,
        position: 'right',
        formatter: function(p) {
          var labels = { 10: 'Pass', 7: 'Warn', 6: 'Warn', 4: 'Fail', 3: 'Fail' };
          return labels[p.value] || '';
        },
        color: muted,
        fontSize: 11,
        fontWeight: 600
      }
    }]
  });
  window.addEventListener('resize', function() { chart1.resize(); });

  // --- Chart 2: Sitemap Coverage (grouped bar) ---
  var chart2 = echarts.init(document.getElementById('chart-sitemap'), null, { renderer: 'svg' });
  chart2.setOption({
    animation: false,
    tooltip: {
      appendToBody: true,
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: bg2,
      borderColor: rule,
      textStyle: { color: ink, fontSize: 13 }
    },
    legend: {
      data: ['Actual Articles', 'In Sitemap', 'Missing'],
      textStyle: { color: muted, fontSize: 12 },
      top: 0,
      right: 0
    },
    grid: { left: 50, right: 20, top: 40, bottom: 30 },
    xAxis: {
      type: 'category',
      data: ['English', 'zh-CN', 'zh-TW'],
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: muted, fontSize: 12 }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: muted, fontSize: 11 },
      splitLine: { lineStyle: { color: rule, type: 'dashed' } }
    },
    series: [
      {
        name: 'Actual Articles',
        type: 'bar',
        barWidth: 18,
        data: [974, 974, 974],
        itemStyle: { color: accent }
      },
      {
        name: 'In Sitemap',
        type: 'bar',
        barWidth: 18,
        data: [806, 806, 806],
        itemStyle: { color: accent2 }
      },
      {
        name: 'Missing',
        type: 'bar',
        barWidth: 18,
        data: [168, 168, 168],
        itemStyle: { color: fail }
      }
    ]
  });
  window.addEventListener('resize', function() { chart2.resize(); });

  // --- Chart 3: Title Tag Quality (stacked bar) ---
  var chart3 = echarts.init(document.getElementById('chart-titles'), null, { renderer: 'svg' });
  chart3.setOption({
    animation: false,
    tooltip: {
      appendToBody: true,
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: bg2,
      borderColor: rule,
      textStyle: { color: ink, fontSize: 13 }
    },
    legend: {
      data: ['With brand suffix', 'Missing brand suffix', 'Too long (>60 chars)'],
      textStyle: { color: muted, fontSize: 12 },
      top: 0,
      right: 0
    },
    grid: { left: 60, right: 20, top: 45, bottom: 30 },
    xAxis: {
      type: 'category',
      data: ['English', 'zh-CN', 'zh-TW'],
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: muted, fontSize: 12 }
    },
    yAxis: {
      type: 'value',
      max: 1000,
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: muted, fontSize: 11 },
      splitLine: { lineStyle: { color: rule, type: 'dashed' } }
    },
    series: [
      {
        name: 'With brand suffix',
        type: 'bar',
        stack: 'total',
        barWidth: 36,
        data: [326, 5, 20],
        itemStyle: { color: pass }
      },
      {
        name: 'Missing brand suffix',
        type: 'bar',
        stack: 'total',
        barWidth: 36,
        data: [648, 969, 954],
        itemStyle: { color: fail }
      },
      {
        name: 'Too long (>60 chars)',
        type: 'bar',
        barWidth: 36,
        data: [397, 410, 385],
        itemStyle: { color: warn }
      }
    ]
  });
  window.addEventListener('resize', function() { chart3.resize(); });

})();
