// SEO & GEO Strategy 2026 — Charts
(function() {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();

  // === Chart 1: Topic Cluster Architecture (Sunburst) ===
  var chart1 = echarts.init(document.getElementById('chart-topic-cluster'), null, { renderer: 'svg' });
  chart1.setOption({
    tooltip: { trigger: 'item', appendToBody: true },
    series: [{
      type: 'sunburst',
      radius: ['15%', '90%'],
      sort: null,
      emphasis: { focus: 'ancestor' },
      levels: [
        {},
        {
          r0: '15%', r: '45%',
          itemStyle: { borderWidth: 2, borderColor: '#fff', gapWidth: 2 },
          label: { rotate: 'tangential', fontSize: 11, fontWeight: 600, color: '#fff' }
        },
        {
          r0: '45%', r: '90%',
          label: { align: 'right', fontSize: 10, color: ink }
        }
      ],
      data: [
        {
          name: 'Beehive Content Hub',
          itemStyle: { color: accent },
          children: [
            {
              name: 'Conversational BI',
              itemStyle: { color: '#d97706' },
              children: [
                { name: 'NL2SQL', value: 1 },
                { name: 'Multi-turn Chat', value: 1 },
                { name: 'Dashboards vs Chat', value: 1 },
                { name: 'Semantic Layer', value: 1 },
                { name: 'Auto Viz', value: 1 },
                { name: 'Data Foundation', value: 1 }
              ]
            },
            {
              name: 'MCP Protocol',
              itemStyle: { color: '#0f766e' },
              children: [
                { name: 'Architecture', value: 1 },
                { name: 'Connectors', value: 1 },
                { name: 'Security', value: 1 },
                { name: 'Build vs Buy', value: 1 },
                { name: 'Open Source', value: 1 }
              ]
            },
            {
              name: 'Industry Verticals',
              itemStyle: { color: '#7c3aed' },
              children: [
                { name: 'Retail Analytics', value: 1 },
                { name: 'Financial Risk', value: 1 },
                { name: 'Manufacturing IoT', value: 1 },
                { name: 'Professional Services', value: 1 },
                { name: 'Real Estate', value: 1 }
              ]
            },
            {
              name: 'Enterprise AI',
              itemStyle: { color: '#dc2626' },
              children: [
                { name: 'Governance', value: 1 },
                { name: 'Change Mgmt', value: 1 },
                { name: 'ROI Framework', value: 1 },
                { name: 'MLOps', value: 1 },
                { name: 'Zero Trust', value: 1 }
              ]
            },
            {
              name: 'Lead Gen',
              itemStyle: { color: '#2563eb' },
              children: [
                { name: 'Beehive vs Tableau', value: 1 },
                { name: 'TCO Analysis', value: 1 },
                { name: 'Case Studies', value: 1 },
                { name: 'Demo Booking', value: 1 }
              ]
            }
          ]
        }
      ]
    }],
    animation: false
  });
  window.addEventListener('resize', function() { chart1.resize(); });

  // === Chart 2: KPI Targets by Phase (Grouped Bar) ===
  var chart2 = echarts.init(document.getElementById('chart-kpis'), null, { renderer: 'svg' });
  chart2.setOption({
    tooltip: { trigger: 'axis', appendToBody: true },
    legend: { data: ['Baseline', 'Month 2', 'Month 4', 'Month 6'], bottom: 0 },
    grid: { left: 80, right: 30, top: 20, bottom: 50 },
    xAxis: {
      type: 'category',
      data: ['Organic Impressions', 'Organic Clicks', 'Indexed Pages', 'Blog Articles', 'AI Citations'],
      axisLabel: { fontSize: 10, color: muted, rotate: 15 }
    },
    yAxis: {
      type: 'value',
      axisLabel: { fontSize: 10, color: muted }
    },
    series: [
      {
        name: 'Baseline',
        type: 'bar',
        barMaxWidth: 20,
        itemStyle: { color: rule },
        data: [100, 100, 200, 56, 0]
      },
      {
        name: 'Month 2',
        type: 'bar',
        barMaxWidth: 20,
        itemStyle: { color: bg2 },
        data: [125, 115, 210, 64, 5]
      },
      {
        name: 'Month 4',
        type: 'bar',
        barMaxWidth: 20,
        itemStyle: { color: accent + 'aa' },
        data: [175, 150, 240, 80, 15]
      },
      {
        name: 'Month 6',
        type: 'bar',
        barMaxWidth: 20,
        itemStyle: { color: accent },
        data: [250, 220, 300, 110, 30]
      }
    ],
    animation: false
  });
  window.addEventListener('resize', function() { chart2.resize(); });
})();
