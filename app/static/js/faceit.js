document.addEventListener('DOMContentLoaded', () => {
  const form   = document.getElementById('faceitForm');
  const result = document.getElementById('result');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const steamLink = document.getElementById('steamLink').value.trim();
    if (!steamLink) return;

    try {
      const res = await fetch('/api/faceit/stats', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ steam_link: steamLink })
      });

      // ВАЖНО: парсим JSON ДО проверки res.ok
      const data = await res.json();

      if (!res.ok) {
        // payload.error содержит строку с ошибкой
        throw new Error(data.error || 'Unknown error');
      }
      
      result.innerHTML = `
        <div class="card" style="display:block;">
          <div class="top">
            <img class="avatar" src="${data.avatar}" alt="avatar">
            <div class="user">
              <a class="name" href="https://www.faceit.com/ru/players/${data.nickname}">
                ${data.nickname}
                <img class="lvl-icon" src="/static/icons/${data.level}.png" alt="lvl">
                <span class="elo">${data.elo}</span>
              </a><br>
              <a class="steam" href="https://steamcommunity.com/profiles/${data.steamid}">Steam</a>
            </div>
          </div>
          <div class="stats">
            <div class="stat"><div class="label">Kills</div><div class="value">${data.kills}</div></div>
            <div class="stat"><div class="label">Assists</div><div class="value">${data.assists}</div></div>
            <div class="stat"><div class="label">Deaths</div><div class="value">${data.deaths}</div></div>
            <div class="stat"><div class="label">K/D</div><div class="value">${data.kd}</div></div>
            <div class="stat"><div class="label">K/R</div><div class="value">${data.kr}</div></div>
            <div class="stat"><div class="label">ADR</div><div class="value">${data.adr}</div></div>
          </div>
        </div>
      `;
    } catch (err) {
      result.innerHTML = `<p style="color:red;">${err.message}</p>`;
    }
  });
});