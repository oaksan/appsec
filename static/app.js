/**
 * Zeppelin-AppSec: Frontend Client Logic, Audit Management & Chart.js Visualizations
 */

document.addEventListener('DOMContentLoaded', () => {
  // Estado da aplicação
  let currentDiagnosticData = null;
  let benchmarkData = null;
  let radarChartInstance = null;
  let barChartInstance = null;
  let activeDimensionFilter = 'all';
  let activeStageFilter = 'all';
  let searchQuery = '';
  let isEditingAudit = false;
  let pendingAnswers = {}; // Map statement_code -> new level (int 0..4)

  // Elementos do DOM - Cabeçalho e Seleção de Squad
  const squadSelect = document.getElementById('squad-select');
  const btnOpenSquadModal = document.getElementById('btn-open-squad-modal');
  const btnOpenSquadModalBtn = document.getElementById('btn-open-squad-modal-btn');
  const squadPurdueBadge = document.getElementById('squad-purdue-badge');
  const squadNameTitle = document.getElementById('squad-name-title');
  const squadDescription = document.getElementById('squad-description');

  // Elementos do DOM - KPIs
  const kpiAdGlobal = document.getElementById('kpi-ad-global');
  const kpiAdProgress = document.getElementById('kpi-ad-progress');
  const kpiPurdueShort = document.getElementById('kpi-purdue-short');
  const kpiPurdueLevelFull = document.getElementById('kpi-purdue-level-full');
  const kpiPredominantStage = document.getElementById('kpi-predominant-stage');

  const countAl0 = document.getElementById('count-al0');
  const countAl1 = document.getElementById('count-al1');
  const countAl2 = document.getElementById('count-al2');
  const countAl3 = document.getElementById('count-al3');
  const countAl4 = document.getElementById('count-al4');

  // Elementos do DOM - Catálogo e Auditoria
  const statementsTableBody = document.getElementById('statements-table-body');
  const statementSearch = document.getElementById('statement-search');
  const dimPills = document.querySelectorAll('.filter-dim-pill');
  const stagePills = document.querySelectorAll('.filter-stage-pill');
  const btnEditAudit = document.getElementById('btn-edit-audit');
  const btnEditText = document.getElementById('btn-edit-text');
  const btnCancelAudit = document.getElementById('btn-cancel-audit');
  const auditStatusBadge = document.getElementById('audit-status-badge');
  const iconEdit = document.getElementById('icon-edit');

  // Elementos do DOM - Benchmark
  const btnBenchmarkToggle = document.getElementById('btn-benchmark-toggle');
  const btnCloseBenchmark = document.getElementById('btn-close-benchmark');
  const benchmarkSection = document.getElementById('benchmark-section');
  const benchmarkDimThead = document.getElementById('benchmark-dim-thead');
  const benchmarkTableBody = document.getElementById('benchmark-table-body');
  const benchmarkDimTfoot = document.getElementById('benchmark-dim-tfoot');
  const benchmarkStagesThead = document.getElementById('benchmark-stages-thead');
  const benchmarkStagesTbody = document.getElementById('benchmark-stages-tbody');
  const benchmarkStagesTfoot = document.getElementById('benchmark-stages-tfoot');

  // Elementos do DOM - Modal Nova Squad
  const squadModal = document.getElementById('squad-modal');
  const btnCloseSquadModal = document.getElementById('btn-close-squad-modal');
  const btnCancelSquadModal = document.getElementById('btn-cancel-squad-modal');
  const squadCreateForm = document.getElementById('squad-create-form');
  const squadModalError = document.getElementById('squad-modal-error');
  const modalSquadName = document.getElementById('modal-squad-name');
  const modalSquadPurdue = document.getElementById('modal-squad-purdue');
  const modalSquadShort = document.getElementById('modal-squad-short');
  const modalSquadDescription = document.getElementById('modal-squad-description');

  // Elementos do DOM - Exclusão de Squad
  const btnDeleteSquad = document.getElementById('btn-delete-squad');
  const deleteSquadModal = document.getElementById('delete-squad-modal');
  const deleteSquadTargetName = document.getElementById('delete-squad-target-name');
  const deleteSquadError = document.getElementById('delete-squad-error');
  const btnCancelDeleteSquad = document.getElementById('btn-cancel-delete-squad');
  const btnConfirmDeleteSquad = document.getElementById('btn-confirm-delete-squad');

  // Mapeamentos de pesos e nomes da escala AL
  const AL_WEIGHTS = { 0: 0.0, 1: 0.1, 2: 0.3, 3: 0.6, 4: 1.0 };
  const AL_PERCENT_STRINGS = { 0: '0%', 1: '10%', 2: '30%', 3: '60%', 4: '100%' };
  const AL_NAMES = {
    0: 'Não Adotada',
    1: 'Abandonada',
    2: 'Projeto / Produto',
    3: 'Processo Definido',
    4: 'Institucionalizada'
  };

  // ---------------------------------------------------------------------------
  // 1. Carregamento de Dados da Squad
  // ---------------------------------------------------------------------------

  async function loadSquadDiagnostic(squadCode) {
    try {
      if (isEditingAudit) {
        toggleEditMode(false);
      }
      const response = await fetch(`/api/diagnostics/${squadCode}`);
      if (!response.ok) {
        throw new Error(`Erro ${response.status} ao carregar diagnóstico.`);
      }
      currentDiagnosticData = await response.json();
      updateDashboardUI(currentDiagnosticData);
    } catch (error) {
      console.error('Falha ao obter diagnóstico:', error);
      showStatusBadge('Não foi possível carregar os dados da squad.', 'error');
    }
  }

  // ---------------------------------------------------------------------------
  // 2. Atualização dos Cards de Métricas e Metadados
  // ---------------------------------------------------------------------------

  function updateDashboardUI(data) {
    // Cabeçalho da squad
    squadNameTitle.textContent = `${data.squad.name} (${data.squad.purdue_short})`;
    squadPurdueBadge.textContent = data.squad.purdue_short;
    squadDescription.textContent = data.squad.description || 'Sem descrição cadastrada.';

    // KPI Cards
    kpiAdGlobal.textContent = data.global_adoption_degree_formatted;
    kpiAdProgress.style.width = `${Math.min(data.global_adoption_degree, 100)}%`;

    kpiPurdueShort.textContent = data.squad.purdue_short;
    kpiPurdueLevelFull.textContent = data.squad.purdue_level;

    kpiPredominantStage.textContent = data.predominant_stage;

    // Contagens AL0-AL4
    countAl0.textContent = data.al_distribution.AL0 || 0;
    countAl1.textContent = data.al_distribution.AL1 || 0;
    countAl2.textContent = data.al_distribution.AL2 || 0;
    countAl3.textContent = data.al_distribution.AL3 || 0;
    countAl4.textContent = data.al_distribution.AL4 || 0;

    // Gráficos
    renderRadarChart(data);
    renderBarChart(data);

    // Tabela de Afirmações
    filterAndRenderStatements();
  }

  // ---------------------------------------------------------------------------
  // 3. Gráfico Radar SMAF (Chart.js)
  // ---------------------------------------------------------------------------

  function renderRadarChart(data) {
    const ctx = document.getElementById('radarChart').getContext('2d');

    const labels = data.dimension_scores.map(d => d.dimension);
    const values = data.dimension_scores.map(d => d.adoption_degree);

    // Média Organizacional de referência (Tabela 4.1 da dissertação)
    const orgAverageValues = [61.7, 42.5, 56.7, 55.0, 43.8, 52.5];

    if (radarChartInstance) {
      radarChartInstance.destroy();
    }

    radarChartInstance = new Chart(ctx, {
      type: 'radar',
      data: {
        labels: labels,
        datasets: [
          {
            label: `${data.squad.name} (${data.squad.purdue_short})`,
            data: values,
            fill: true,
            backgroundColor: 'rgba(68, 114, 196, 0.25)',
            borderColor: '#1B365D',
            pointBackgroundColor: '#4472C4',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: '#1B365D',
            borderWidth: 2.5,
            pointRadius: 4,
          },
          {
            label: 'Média Organizacional (52,0%)',
            data: orgAverageValues,
            fill: false,
            borderColor: '#94A3B8',
            borderDash: [5, 5],
            borderWidth: 1.5,
            pointRadius: 2,
            pointBackgroundColor: '#94A3B8',
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              boxWidth: 14,
              font: { size: 11, family: 'system-ui' },
              color: '#334155'
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => ` ${context.dataset.label}: ${context.raw.toFixed(1)}%`
            }
          }
        },
        scales: {
          r: {
            min: 0,
            max: 100,
            ticks: {
              stepSize: 20,
              backdropColor: 'transparent',
              font: { size: 10 },
              color: '#64748B',
              callback: (value) => `${value}%`
            },
            grid: { color: '#E2E8F0' },
            angleLines: { color: '#E2E8F0' },
            pointLabels: {
              font: { size: 11, weight: '600' },
              color: '#1E293B'
            }
          }
        }
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 4. Gráfico de Barras Empilhadas StH-AppSec (Chart.js)
  // ---------------------------------------------------------------------------

  function renderBarChart(data) {
    const ctx = document.getElementById('barChart').getContext('2d');

    const stageLabels = data.stage_scores.map(s => s.stage.replace(' (Reactive)', ' (Reat.)').replace(' (Continuous Security Integration)', ''));

    const al0Counts = data.stage_scores.map(s => s.al_counts.AL0 || 0);
    const al1Counts = data.stage_scores.map(s => s.al_counts.AL1 || 0);
    const al2Counts = data.stage_scores.map(s => s.al_counts.AL2 || 0);
    const al3Counts = data.stage_scores.map(s => s.al_counts.AL3 || 0);
    const al4Counts = data.stage_scores.map(s => s.al_counts.AL4 || 0);

    if (barChartInstance) {
      barChartInstance.destroy();
    }

    barChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: stageLabels,
        datasets: [
          {
            label: 'AL0 - Não Adotada (0%)',
            data: al0Counts,
            backgroundColor: '#CBD5E1',
          },
          {
            label: 'AL1 - Abandonada (10%)',
            data: al1Counts,
            backgroundColor: '#94A3B8',
          },
          {
            label: 'AL2 - Projeto (30%)',
            data: al2Counts,
            backgroundColor: '#93C5FD',
          },
          {
            label: 'AL3 - Processo (60%)',
            data: al3Counts,
            backgroundColor: '#3B82F6',
          },
          {
            label: 'AL4 - Institucionalizada (100%)',
            data: al4Counts,
            backgroundColor: '#10B981',
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              boxWidth: 12,
              font: { size: 10, family: 'system-ui' },
              color: '#334155'
            }
          },
          tooltip: {
            mode: 'index',
            intersect: false
          }
        },
        scales: {
          x: {
            stacked: true,
            grid: { display: false },
            ticks: {
              font: { size: 11, weight: '500' },
              color: '#1E293B'
            }
          },
          y: {
            stacked: true,
            beginAtZero: true,
            max: 12,
            ticks: {
              stepSize: 2,
              font: { size: 10 },
              color: '#64748B'
            },
            grid: { color: '#F1F5F9' },
            title: {
              display: true,
              text: 'Quantidade de Práticas',
              font: { size: 11 }
            }
          }
        }
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 5. Renderização da Tabela de 40 Afirmações com Edição e Filtros Combinados
  // ---------------------------------------------------------------------------

  function getBadgeClasses(alCode) {
    switch (alCode) {
      case 'AL4':
        return 'bg-emerald-100 text-emerald-800 border border-emerald-300 font-extrabold';
      case 'AL3':
        return 'bg-blue-100 text-blue-900 border border-blue-300 font-bold';
      case 'AL2':
        return 'bg-sky-50 text-sky-800 border border-sky-200 font-semibold';
      case 'AL1':
        return 'bg-slate-200 text-slate-700 border border-slate-300';
      case 'AL0':
      default:
        return 'bg-slate-100 text-slate-500 border border-slate-200';
    }
  }

  function filterAndRenderStatements() {
    if (!currentDiagnosticData || !currentDiagnosticData.statements) return;

    let items = currentDiagnosticData.statements;

    // 1. Filtro por Dimensão SMAF
    if (activeDimensionFilter !== 'all') {
      items = items.filter(item => item.smaf_dimension === activeDimensionFilter);
    }

    // 2. Filtro por Estágio StH-AppSec
    if (activeStageFilter !== 'all') {
      items = items.filter(item => item.sth_stage_code === activeStageFilter);
    }

    // 3. Filtro por Busca de Texto
    if (searchQuery.trim() !== '') {
      const q = searchQuery.toLowerCase();
      items = items.filter(item =>
        item.statement_code.toLowerCase().includes(q) ||
        item.description.toLowerCase().includes(q) ||
        item.samm_ref.toLowerCase().includes(q) ||
        item.dsomm_ref.toLowerCase().includes(q)
      );
    }

    if (items.length === 0) {
      statementsTableBody.innerHTML = `
        <tr>
          <td colspan="7" class="py-12 text-center text-slate-500">
            <div class="flex flex-col items-center justify-center gap-2">
              <svg class="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <p class="font-medium text-sm">Nenhuma afirmação encontrada para os filtros selecionados.</p>
              <button id="btn-reset-filters" class="mt-2 text-xs font-semibold text-zsteel hover:text-znavy underline">
                Limpar todos os filtros
              </button>
            </div>
          </td>
        </tr>
      `;
      const btnReset = document.getElementById('btn-reset-filters');
      if (btnReset) {
        btnReset.addEventListener('click', resetAllFilters);
      }
      return;
    }

    statementsTableBody.innerHTML = items.map((item, idx) => {
      const rowBg = idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/60';
      const currentLevel = pendingAnswers[item.statement_code] !== undefined
        ? pendingAnswers[item.statement_code]
        : item.adoption_level_num;

      const currentCode = `AL${currentLevel}`;
      const badgeClass = getBadgeClasses(currentCode);
      const currentPct = AL_PERCENT_STRINGS[currentLevel] || '0%';

      // Célula do Nível AL: estática ou interativa
      let levelCellHtml = '';
      if (isEditingAudit) {
        levelCellHtml = `
          <select data-code="${item.statement_code}" class="al-level-select text-xs font-bold px-2 py-1 rounded border border-slate-300 focus:outline-none focus:ring-2 focus:ring-zroyal bg-white text-slate-800 shadow-sm cursor-pointer">
            <option value="0" ${currentLevel === 0 ? 'selected' : ''}>AL0 - Não Adotada (0%)</option>
            <option value="1" ${currentLevel === 1 ? 'selected' : ''}>AL1 - Abandonada (10%)</option>
            <option value="2" ${currentLevel === 2 ? 'selected' : ''}>AL2 - Projeto (30%)</option>
            <option value="3" ${currentLevel === 3 ? 'selected' : ''}>AL3 - Processo (60%)</option>
            <option value="4" ${currentLevel === 4 ? 'selected' : ''}>AL4 - Institucionalizada (100%)</option>
          </select>
        `;
      } else {
        levelCellHtml = `
          <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] ${badgeClass}">
            ${currentCode}
          </span>
        `;
      }

      return `
        <tr class="${rowBg} hover:bg-blue-50/50 transition" data-statement="${item.statement_code}">
          <td class="py-3 px-4 font-mono font-bold text-zsteel">${item.statement_code}</td>
          <td class="py-3 px-4 text-slate-800 font-medium">${item.description}</td>
          <td class="py-3 px-4">
            <span class="inline-block px-2 py-0.5 rounded text-[11px] bg-slate-100 text-slate-700 font-medium">
              ${item.smaf_dimension}
            </span>
          </td>
          <td class="py-3 px-4 text-[11px] text-slate-600">${item.sth_stage}</td>
          <td class="py-3 px-4 text-center al-cell">
            ${levelCellHtml}
          </td>
          <td class="py-3 px-4 text-center font-bold text-slate-800 ad-cell" id="ad-cell-${item.statement_code}">${currentPct}</td>
          <td class="py-3 px-4 text-[11px] text-slate-500 space-y-0.5">
            <div><strong class="text-slate-700">SAMM:</strong> ${item.samm_ref}</div>
            <div><strong class="text-slate-700">DSOMM:</strong> ${item.dsomm_ref}</div>
          </td>
        </tr>
      `;
    }).join('');

    // Adiciona listener aos selects caso esteja em modo de edição
    if (isEditingAudit) {
      const selects = statementsTableBody.querySelectorAll('.al-level-select');
      selects.forEach(sel => {
        sel.addEventListener('change', (e) => {
          const code = e.target.getAttribute('data-code');
          const newLevel = parseInt(e.target.value, 10);
          pendingAnswers[code] = newLevel;

          // Atualiza a coluna de porcentagem adjacente dinamicamente
          const adCell = document.getElementById(`ad-cell-${code}`);
          if (adCell) {
            adCell.textContent = AL_PERCENT_STRINGS[newLevel] || '0%';
          }
        });
      });
    }
  }

  function resetAllFilters() {
    activeDimensionFilter = 'all';
    activeStageFilter = 'all';
    searchQuery = '';
    statementSearch.value = '';

    dimPills.forEach(p => {
      p.classList.remove('bg-znavy', 'text-white', 'active');
      p.classList.add('bg-white', 'text-slate-700');
      if (p.getAttribute('data-dim') === 'all') {
        p.classList.remove('bg-white', 'text-slate-700');
        p.classList.add('bg-znavy', 'text-white', 'active');
      }
    });

    stagePills.forEach(p => {
      p.classList.remove('bg-znavy', 'text-white', 'active');
      p.classList.add('bg-white', 'text-slate-700');
      if (p.getAttribute('data-stage') === 'all') {
        p.classList.remove('bg-white', 'text-slate-700');
        p.classList.add('bg-znavy', 'text-white', 'active');
      }
    });

    filterAndRenderStatements();
  }

  // ---------------------------------------------------------------------------
  // 6. Modo de Edição e Persistência de Auditoria (US1)
  // ---------------------------------------------------------------------------

  function toggleEditMode(editing) {
    isEditingAudit = editing;

    if (isEditingAudit) {
      pendingAnswers = {};
      btnEditText.textContent = 'Salvar Alterações';
      btnEditAudit.className = 'inline-flex items-center justify-center gap-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold px-3.5 py-2 rounded-lg transition shadow-sm';
      iconEdit.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>';
      btnCancelAudit.classList.remove('hidden');
      showStatusBadge('Modo de edição ativo: altere os níveis AL e clique em Salvar.', 'info');
    } else {
      pendingAnswers = {};
      btnEditText.textContent = 'Editar Auditoria';
      btnEditAudit.className = 'inline-flex items-center justify-center gap-1.5 bg-zsteel hover:bg-zroyal text-white text-xs font-semibold px-3.5 py-2 rounded-lg transition shadow-sm';
      iconEdit.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>';
      btnCancelAudit.classList.add('hidden');
    }

    filterAndRenderStatements();
  }

  async function saveAuditChanges() {
    if (Object.keys(pendingAnswers).length === 0) {
      toggleEditMode(false);
      showStatusBadge('Nenhuma alteração pendente.', 'info');
      return;
    }

    const squadCode = squadSelect.value;
    const payload = {
      answers: Object.entries(pendingAnswers).map(([code, level]) => ({
        statement_code: code,
        adoption_level: level
      }))
    };

    showStatusBadge('Salvando alterações no banco local...', 'loading');

    try {
      const response = await fetch(`/api/diagnostics/${squadCode}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `Erro ${response.status} ao salvar.`);
      }

      currentDiagnosticData = await response.json();
      toggleEditMode(false);
      updateDashboardUI(currentDiagnosticData);
      showStatusBadge('Auditoria salva com sucesso e persistida no banco local!', 'success');

      // Se a seção de benchmark estiver visível, recarrega os dados consolidados
      if (!benchmarkSection.classList.contains('hidden')) {
        loadBenchmarkData();
      }
    } catch (err) {
      console.error('Erro ao salvar auditoria:', err);
      showStatusBadge(`Falha ao salvar: ${err.message}`, 'error');
    }
  }

  function showStatusBadge(message, type = 'info') {
    auditStatusBadge.classList.remove('hidden', 'bg-blue-100', 'text-blue-800', 'bg-emerald-100', 'text-emerald-800', 'bg-red-100', 'text-red-800');
    auditStatusBadge.textContent = message;

    if (type === 'success') {
      auditStatusBadge.classList.add('bg-emerald-100', 'text-emerald-800');
    } else if (type === 'error') {
      auditStatusBadge.classList.add('bg-red-100', 'text-red-800');
    } else {
      auditStatusBadge.classList.add('bg-blue-100', 'text-blue-800');
    }

    if (type === 'success' || type === 'info') {
      setTimeout(() => {
        if (!isEditingAudit) {
          auditStatusBadge.classList.add('hidden');
        }
      }, 4000);
    }
  }

  // ---------------------------------------------------------------------------
  // 7. Modal e Cadastro de Nova Squad (US2)
  // ---------------------------------------------------------------------------

  function openSquadModal() {
    squadCreateForm.reset();
    squadModalError.classList.add('hidden');
    squadModalError.textContent = '';
    squadModal.classList.remove('hidden');
    modalSquadName.focus();
  }

  function closeSquadModal() {
    squadModal.classList.add('hidden');
  }

  async function handleSquadCreateSubmit(e) {
    e.preventDefault();
    squadModalError.classList.add('hidden');

    const name = modalSquadName.value.trim();
    const purdueLevel = modalSquadPurdue.value.trim();
    const purdueShort = modalSquadShort.value.trim();
    const description = modalSquadDescription.value.trim();

    if (!name || !purdueLevel || !purdueShort) {
      squadModalError.textContent = 'Por favor, preencha todos os campos obrigatórios (*).';
      squadModalError.classList.remove('hidden');
      return;
    }

    try {
      const response = await fetch('/api/squads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name,
          purdue_level: purdueLevel,
          purdue_short: purdueShort,
          description: description
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Erro ${response.status} ao cadastrar squad.`);
      }

      const newSquad = await response.json();

      // Adiciona a nova opção no seletor e seleciona-a
      const newOption = document.createElement('option');
      newOption.value = newSquad.code;
      newOption.textContent = `${newSquad.name} (${newSquad.purdue_short})`;
      squadSelect.appendChild(newOption);
      squadSelect.value = newSquad.code;

      closeSquadModal();
      showStatusBadge(`Nova squad "${newSquad.name}" cadastrada com 40 afirmações em AL0!`, 'success');

      // Carrega o diagnóstico inicial da nova squad
      await loadSquadDiagnostic(newSquad.code);

      // Atualiza o benchmark caso esteja aberto
      if (!benchmarkSection.classList.contains('hidden')) {
        loadBenchmarkData();
      }
    } catch (err) {
      console.error('Falha ao criar squad:', err);
      squadModalError.textContent = err.message;
      squadModalError.classList.remove('hidden');
    }
  }

  // ---------------------------------------------------------------------------
  // 7.1. Modal e Exclusão de Squad (US5)
  // ---------------------------------------------------------------------------

  function openDeleteSquadModal() {
    if (squadSelect.options.length <= 1) {
      showStatusBadge('Não é permitido excluir a única squad do sistema.', 'error');
      return;
    }
    const currentName = currentDiagnosticData?.squad?.name || squadSelect.options[squadSelect.selectedIndex]?.text;
    deleteSquadTargetName.textContent = currentName;
    deleteSquadError.classList.add('hidden');
    deleteSquadError.textContent = '';
    deleteSquadModal.classList.remove('hidden');
  }

  function closeDeleteSquadModal() {
    deleteSquadModal.classList.add('hidden');
  }

  async function handleDeleteSquadConfirm() {
    const squadCode = squadSelect.value;
    if (!squadCode) return;

    deleteSquadError.classList.add('hidden');
    deleteSquadError.textContent = '';

    try {
      const response = await fetch(`/api/squads/${squadCode}`, {
        method: 'DELETE'
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `Erro ${response.status} ao excluir squad.`);
      }

      const resData = await response.json();
      closeDeleteSquadModal();
      showStatusBadge(resData.message || 'Squad excluída com sucesso!', 'success');

      // Remove a opção do select
      const opt = squadSelect.querySelector(`option[value="${squadCode}"]`);
      if (opt) {
        opt.remove();
      }

      // Se houver squads remanescentes, seleciona a primeira e recarrega
      if (squadSelect.options.length > 0) {
        squadSelect.selectedIndex = 0;
        await loadSquadDiagnostic(squadSelect.value);
      }

      // Atualiza o benchmark caso esteja aberto
      if (!benchmarkSection.classList.contains('hidden')) {
        loadBenchmarkData();
      }
    } catch (err) {
      console.error('Falha ao excluir squad:', err);
      deleteSquadError.textContent = err.message;
      deleteSquadError.classList.remove('hidden');
    }
  }

  // ---------------------------------------------------------------------------
  // 8. Matrizes de Benchmark Organizacional Dinâmicas (SMAF & StH Tabela 4.2)
  // ---------------------------------------------------------------------------

  async function loadBenchmarkData() {
    try {
      const response = await fetch('/api/benchmark');
      if (!response.ok) throw new Error('Falha ao obter benchmark');
      benchmarkData = await response.json();

      const squads = benchmarkData.squads || [];

      // 1. Tabela de Dimensões SMAF
      benchmarkDimThead.innerHTML = `
        <tr class="bg-znavy text-white text-xs uppercase tracking-wider">
          <th class="py-3 px-4 rounded-tl-lg">Dimensão SMAF</th>
          ${squads.map(sq => `<th class="py-3 px-4 text-center whitespace-nowrap">${sq.name} (${sq.purdue_short})</th>`).join('')}
          <th class="py-3 px-4 text-center bg-zsteel rounded-tr-lg">Média Geral</th>
        </tr>
      `;

      benchmarkTableBody.innerHTML = benchmarkData.dimensions.map((row, idx) => {
        const bg = idx % 2 === 0 ? 'bg-white' : 'bg-slate-50';
        return `
          <tr class="${bg} hover:bg-blue-50/40 transition">
            <td class="py-3 px-4 font-semibold text-slate-800">${row.dimension}</td>
            ${squads.map(sq => {
              const val = row.scores && row.scores[sq.code] !== undefined ? row.scores[sq.code] : (
                sq.code === 'squad-a' ? row.squad_a_pct :
                sq.code === 'squad-b' ? row.squad_b_pct :
                sq.code === 'squad-c' ? row.squad_c_pct : 0.0
              );
              return `<td class="py-3 px-4 text-center">${val.toFixed(1)}%</td>`;
            }).join('')}
            <td class="py-3 px-4 text-center font-bold text-znavy bg-slate-100/80">${row.average_pct.toFixed(1)}%</td>
          </tr>
        `;
      }).join('');

      benchmarkDimTfoot.innerHTML = `
        <tr class="bg-zice font-bold text-znavy border-t-2 border-zsteel">
          <td class="py-3.5 px-4 rounded-bl-lg font-extrabold">GRAU DE ADOÇÃO GLOBAL (AD%)</td>
          ${squads.map(sq => {
            const val = benchmarkData.global_summary.scores && benchmarkData.global_summary.scores[sq.code] !== undefined
              ? benchmarkData.global_summary.scores[sq.code]
              : (
                sq.code === 'squad-a' ? benchmarkData.global_summary.squad_a_pct :
                sq.code === 'squad-b' ? benchmarkData.global_summary.squad_b_pct :
                sq.code === 'squad-c' ? benchmarkData.global_summary.squad_c_pct : 0.0
              );
            return `<td class="py-3.5 px-4 text-center font-extrabold text-blue-900">${val.toFixed(1)}%</td>`;
          }).join('')}
          <td class="py-3.5 px-4 text-center font-black bg-blue-200 text-znavy rounded-br-lg text-base">
            ${benchmarkData.global_summary.organization_average_pct.toFixed(1)}%
          </td>
        </tr>
      `;

      // 2. Tabela de Estágios StH-AppSec (Tabela 4.2 da dissertação)
      benchmarkStagesThead.innerHTML = `
        <tr class="bg-zsteel text-white text-xs uppercase tracking-wider">
          <th class="py-3 px-4 rounded-tl-lg">Estágio StH-AppSec</th>
          ${squads.map(sq => `<th class="py-3 px-4 text-center whitespace-nowrap">${sq.name} (${sq.purdue_short})</th>`).join('')}
          <th class="py-3 px-4 text-center bg-znavy rounded-tr-lg">Média Geral</th>
        </tr>
      `;

      benchmarkStagesTbody.innerHTML = benchmarkData.stages.map((row, idx) => {
        const bg = idx % 2 === 0 ? 'bg-white' : 'bg-slate-50';
        return `
          <tr class="${bg} hover:bg-blue-50/40 transition">
            <td class="py-3 px-4 font-semibold text-slate-800">
              <span class="inline-block w-2 h-2 rounded-full bg-zsteel mr-1.5"></span>
              ${row.stage}
            </td>
            ${squads.map(sq => {
              const val = row.scores && row.scores[sq.code] !== undefined ? row.scores[sq.code] : (
                sq.code === 'squad-a' ? row.squad_a_pct :
                sq.code === 'squad-b' ? row.squad_b_pct :
                sq.code === 'squad-c' ? row.squad_c_pct : 0.0
              );
              return `<td class="py-3 px-4 text-center font-medium">${val.toFixed(1)}%</td>`;
            }).join('')}
            <td class="py-3 px-4 text-center font-bold text-znavy bg-slate-100/80">${row.average_pct.toFixed(1)}%</td>
          </tr>
        `;
      }).join('');

      benchmarkStagesTfoot.innerHTML = `
        <tr class="bg-zice font-bold text-znavy border-t-2 border-zsteel">
          <td class="py-3.5 px-4 rounded-bl-lg font-extrabold">GRAU DE ADOÇÃO GLOBAL (AD%)</td>
          ${squads.map(sq => {
            const val = benchmarkData.global_summary.scores && benchmarkData.global_summary.scores[sq.code] !== undefined
              ? benchmarkData.global_summary.scores[sq.code]
              : (
                sq.code === 'squad-a' ? benchmarkData.global_summary.squad_a_pct :
                sq.code === 'squad-b' ? benchmarkData.global_summary.squad_b_pct :
                sq.code === 'squad-c' ? benchmarkData.global_summary.squad_c_pct : 0.0
              );
            return `<td class="py-3.5 px-4 text-center font-extrabold text-blue-900">${val.toFixed(1)}%</td>`;
          }).join('')}
          <td class="py-3.5 px-4 text-center font-black bg-blue-200 text-znavy rounded-br-lg text-base">
            ${benchmarkData.global_summary.organization_average_pct.toFixed(1)}%
          </td>
        </tr>
      `;

    } catch (err) {
      console.error('Erro ao carregar benchmark:', err);
    }
  }

  // ---------------------------------------------------------------------------
  // 9. Event Listeners & Vinculações
  // ---------------------------------------------------------------------------

  // Seleção de Squad
  squadSelect.addEventListener('change', (e) => {
    loadSquadDiagnostic(e.target.value);
  });

  // Modal Nova Squad
  if (btnOpenSquadModal) {
    btnOpenSquadModal.addEventListener('click', openSquadModal);
  }
  if (btnOpenSquadModalBtn) {
    btnOpenSquadModalBtn.addEventListener('click', openSquadModal);
  }
  if (btnCloseSquadModal) {
    btnCloseSquadModal.addEventListener('click', closeSquadModal);
  }
  if (btnCancelSquadModal) {
    btnCancelSquadModal.addEventListener('click', closeSquadModal);
  }
  if (squadCreateForm) {
    squadCreateForm.addEventListener('submit', handleSquadCreateSubmit);
  }

  // Exclusão de Squad
  if (btnDeleteSquad) {
    btnDeleteSquad.addEventListener('click', openDeleteSquadModal);
  }
  if (btnCancelDeleteSquad) {
    btnCancelDeleteSquad.addEventListener('click', closeDeleteSquadModal);
  }
  if (btnConfirmDeleteSquad) {
    btnConfirmDeleteSquad.addEventListener('click', handleDeleteSquadConfirm);
  }

  // Fechar modais ao clicar fora
  window.addEventListener('click', (e) => {
    if (e.target === squadModal) {
      closeSquadModal();
    }
    if (e.target === deleteSquadModal) {
      closeDeleteSquadModal();
    }
  });

  // Modo de Edição de Auditoria
  btnEditAudit.addEventListener('click', () => {
    if (!isEditingAudit) {
      toggleEditMode(true);
    } else {
      saveAuditChanges();
    }
  });

  btnCancelAudit.addEventListener('click', () => {
    toggleEditMode(false);
    showStatusBadge('Edição cancelada. Nenhuma alteração foi salva.', 'info');
  });

  // Busca de Afirmações
  statementSearch.addEventListener('input', (e) => {
    searchQuery = e.target.value;
    filterAndRenderStatements();
  });

  // Filtros por Dimensão SMAF
  dimPills.forEach(pill => {
    pill.addEventListener('click', () => {
      dimPills.forEach(p => {
        p.classList.remove('bg-znavy', 'text-white', 'active');
        p.classList.add('bg-white', 'text-slate-700');
      });
      pill.classList.remove('bg-white', 'text-slate-700');
      pill.classList.add('bg-znavy', 'text-white', 'active');

      activeDimensionFilter = pill.getAttribute('data-dim');
      filterAndRenderStatements();
    });
  });

  // Filtros por Estágio StH-AppSec
  stagePills.forEach(pill => {
    pill.addEventListener('click', () => {
      stagePills.forEach(p => {
        p.classList.remove('bg-znavy', 'text-white', 'active');
        p.classList.add('bg-white', 'text-slate-700');
      });
      pill.classList.remove('bg-white', 'text-slate-700');
      pill.classList.add('bg-znavy', 'text-white', 'active');

      activeStageFilter = pill.getAttribute('data-stage');
      filterAndRenderStatements();
    });
  });

  // Toggle do Drawer de Benchmark
  btnBenchmarkToggle.addEventListener('click', () => {
    const isHidden = benchmarkSection.classList.contains('hidden');
    if (isHidden) {
      benchmarkSection.classList.remove('hidden');
      loadBenchmarkData();
      benchmarkSection.scrollIntoView({ behavior: 'smooth' });
    } else {
      benchmarkSection.classList.add('hidden');
    }
  });

  btnCloseBenchmark.addEventListener('click', () => {
    benchmarkSection.classList.add('hidden');
  });

  // Inicialização Automática
  if (squadSelect.value) {
    loadSquadDiagnostic(squadSelect.value);
  }
});
