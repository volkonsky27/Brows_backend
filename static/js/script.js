// Ждём, когда WebApp готов, затем расширяем
    function onTelegramReady() {
      const tg = window.Telegram.WebApp;
      // Убедиться, что SDK готов
      tg.ready();

      // Попытаться расширить
      if (tg.expand) {
        try {
          tg.expand();
        } catch (e) {
          console.warn("Telegram expand error:", e);
        }
      }
    }

    function formatDate(isoString) {
      const date = new Date(isoString);
      const dd = String(date.getDate()).padStart(2, '0');
      const mm = String(date.getMonth() + 1).padStart(2, '0');
      const yyyy = date.getFullYear();
      const hh = String(date.getHours()).padStart(2, '0');
      const min = String(date.getMinutes()).padStart(2, '0');
      return `${dd}.${mm}.${yyyy} ${hh}:${min}`;
    }

    async function initApp() {
      onTelegramReady();

      const tg = window.Telegram.WebApp;
      const userId = tg.initDataUnsafe?.user?.id;

      const response = await fetch("/myuser", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "user": userId
        }
      });
      const data = await response.json();

      document.getElementById("balance").textContent = data.balance;
      document.getElementById("username").textContent = data.first_name;
      document.getElementById("qr").innerHTML =
        `<img src="${data.image}" alt="QR Code" class="w-64 h-64">`;

      const tbody = document.getElementById("transactions");
      data.transactions.forEach(t => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td class="p-2 border border-gray-200">${formatDate(t.date)}</td>
          <td class="p-2 border border-gray-200">${t.sum_op}</td>
        `;
        tbody.appendChild(tr);
      });
    }

    window.addEventListener("DOMContentLoaded", initApp);
    // Также слушать изменение viewport (на случай изменения) — если SDK поддерживает
    if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.onEvent) {
      window.Telegram.WebApp.onEvent("viewportChanged", () => {
        // Можно снова попытаться expand или перерасчитать стили
        if (window.Telegram.WebApp.expand) {
          window.Telegram.WebApp.expand();
        }
      });
    }

    // При загрузке и изменении размера — проверка прокручиваемости
    window.addEventListener("load", () => {
      const doc = document.documentElement;
      if (doc.scrollHeight <= window.innerHeight) {
        doc.style.setProperty("height", "calc(100vh + 1px)", "important");
      }
    });