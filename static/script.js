const apiBase = 'http://127.0.0.1:5000';

function formatDateForInput(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  if (isNaN(date)) return '';
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

document.addEventListener('DOMContentLoaded', () => {
  const missionForm = document.getElementById('missionForm');
  const searchInput = document.getElementById('searchInput');

  async function loadMissions() {
    const res = await fetch(`${apiBase}/missions`);
    const data = await res.json();
    const table = document.querySelector('tbody');
    table.innerHTML = '';
    data.forEach(m => {
      table.innerHTML += `
        <tr data-mission-id="${m.mission_id}">
          <td>${m.mission_id}</td>
          <td>${m.name}</td>
          <td>${m.agency_id}</td>
          <td>${m.spacecraft_id}</td>
          <td>${m.destination_id}</td>
          <td>${formatDateForInput(m.launch_date)}</td>
          <td>${m.mission_type}</td>
          <td>${m.mission_status}</td>
          <td>
            <button onclick="editMission('${m.mission_id}')">Edit</button>
            <button onclick="deleteMission('${m.mission_id}')">Delete</button>
          </td>
        </tr>`;
    });
  }

  missionForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const mission = {
      mission_id: missionForm.mission_id.value.trim(),
      name: missionForm.name.value.trim(),
      agency_id: missionForm.agency_id.value.trim(),
      spacecraft_id: missionForm.spacecraft_id.value.trim(),
      destination_id: missionForm.destination_id.value.trim(),
      launch_date: missionForm.launch_date.value,
      mission_type: missionForm.mission_type.value.trim(),
      mission_status: missionForm.mission_status.value.trim(),
    };

    if (!mission.mission_id || !mission.name) {
      alert("Mission ID and Name are required");
      return;
    }

    // Check if mission exists to decide update/add
    let res = await fetch(`${apiBase}/missions/${mission.mission_id}`);
    if (res.ok) {
      await fetch(`${apiBase}/missions/${mission.mission_id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mission)
      });
      alert('Mission updated');
    } else {
      await fetch(`${apiBase}/missions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mission)
      });
      alert('Mission added');
    }

    loadMissions();
    missionForm.reset();
  });

  window.editMission = async function(id) {
    const res = await fetch(`${apiBase}/missions/${id}`);
    if (res.ok) {
      const m = await res.json();
      missionForm.mission_id.value = m.mission_id;
      missionForm.name.value = m.name;
      missionForm.agency_id.value = m.agency_id;
      missionForm.spacecraft_id.value = m.spacecraft_id;
      missionForm.destination_id.value = m.destination_id;
      missionForm.launch_date.value = formatDateForInput(m.launch_date);
      missionForm.mission_type.value = m.mission_type;
      missionForm.mission_status.value = m.mission_status;
    } else {
      alert('Mission not found');
    }
  };

  window.deleteMission = async function(id) {
    if (!confirm(`Delete mission ${id}?`)) return;
    await fetch(`${apiBase}/missions/${id}`, { method: 'DELETE' });
    alert('Mission deleted');
    loadMissions();
  };

  window.searchMission = async function() {
    const keyword = searchInput.value.trim();
    if (!keyword) {
      loadMissions();
      return;
    }
    const res = await fetch(`${apiBase}/missions/search?q=${encodeURIComponent(keyword)}`);
    if (res.ok) {
      const data = await res.json();
      const table = document.querySelector('tbody');
      table.innerHTML = '';
      data.forEach(m => {
        table.innerHTML += `
          <tr data-mission-id="${m.mission_id}">
            <td>${m.mission_id}</td>
            <td>${m.name}</td>
            <td>${m.agency_id}</td>
            <td>${m.spacecraft_id}</td>
            <td>${m.destination_id}</td>
            <td>${formatDateForInput(m.launch_date)}</td>
            <td>${m.mission_type}</td>
            <td>${m.mission_status}</td>
            <td>
              <button onclick="editMission('${m.mission_id}')">Edit</button>
              <button onclick="deleteMission('${m.mission_id}')">Delete</button>
            </td>
          </tr>`;
      });
    } else {
      alert('Search failed');
    }
  };

  loadMissions();
});
