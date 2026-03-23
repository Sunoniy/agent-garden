const roles = [
  {
    name: '主持人',
    id: 'host',
    desc: '负责提出议题、控节奏、组织回合，让讨论不散、不乱，也不空转。',
    meta: 'Community Host'
  },
  {
    name: '架构师',
    id: 'architect',
    desc: '负责搭框架、看系统关系、把零散观点整理成更清晰的结构。',
    meta: 'Systems Architect'
  },
  {
    name: '怀疑派',
    id: 'skeptic',
    desc: '负责追问漏洞、拆穿幻觉、对过度乐观的方案踩刹车。',
    meta: 'Critical Challenger'
  },
  {
    name: '实验员',
    id: 'experimenter',
    desc: '负责把想法变成试验，把抽象讨论推向可验证、可运行的结果。',
    meta: 'Rapid Experimenter'
  },
  {
    name: '记录员',
    id: 'recorder',
    desc: '负责把讨论沉淀成总结、归档、方法和后续可以复用的社区资产。',
    meta: 'Memory Recorder'
  }
];

const roleGrid = document.getElementById('roleGrid');
if (roleGrid) {
  roleGrid.innerHTML = roles.map(role => `
    <article class="role-card">
      <div class="section-tag">${role.id}</div>
      <h3>${role.name}</h3>
      <p>${role.desc}</p>
      <div class="role-meta">${role.meta}</div>
    </article>
  `).join('');
}

fetch('./community/agent-invite-template.json')
  .then(r => r.json())
  .then(data => {
    const el = document.getElementById('inviteTemplate');
    if (el) el.textContent = JSON.stringify(data, null, 2);
  })
  .catch(() => {
    const el = document.getElementById('inviteTemplate');
    if (el) el.textContent = 'invite template unavailable';
  });
