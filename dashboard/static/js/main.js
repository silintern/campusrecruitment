document.addEventListener('DOMContentLoaded', function() {
    // Global state for chart instances and current table data
    const charts = {};
    let currentTableData = [];

    // --- Main Application Logic ---

    /**
     * Fetches all dashboard data from the backend and orchestrates the UI update.
     */
    async function fetchDataAndRender() {
        showLoading(true);
        hideError();

        const params = new URLSearchParams();
        document.querySelectorAll('.filter-select').forEach(sel => {
            if (sel.value && sel.value !== 'all') {
                params.append(sel.name, sel.value);
            }
        });

        try {
            const response = await fetch(`/api/data?${params.toString()}`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'An unknown error occurred on the server.');
            }
            
            currentTableData = data.table_data || [];

            if (!document.getElementById('location-filter').dataset.populated) {
                populateFilterOptions(data.filters);
            }

            updateKPIs(data.kpis);
            updateAllCharts(data.charts);
            populateTable(data.table_data, data.all_columns, data.default_columns);
            populateStatusModal(data.table_data);
            
            // Repopulate column selector every time to reflect schema changes
            populateColumnSelector(data.all_columns, data.default_columns);

        } catch (error) {
            console.error('Dashboard Render Error:', error);
            showError(`Failed to load dashboard data. ${error.message}`);
        } finally {
            showLoading(false);
        }
    }

    // --- UI Update Functions (KPIs, Charts, etc. - largely unchanged) ---

    function updateKPIs(kpis = {}) {
        const kpiGrid = document.getElementById('kpi-grid');
        if (!kpiGrid) return;
        kpiGrid.innerHTML = '';
        const kpiMapping = {
            applications: 'No. of Applications', shortlisted: 'No. of Shortlisted',
            interviewed: 'No. of Interviewed', offered: 'No. of Offered',
            hired: 'No. of Hired', rejected: 'No. of Rejected',
            acceptance_rate: 'Acceptance Rate (%)', rejection_rate: 'Rejection Rate (%)'
        };
        for (const key in kpiMapping) {
            const card = document.createElement('div');
            card.className = 'bg-white p-4 rounded-lg shadow text-center';
            const value = kpis[key] !== undefined ? kpis[key] : '0';
            card.innerHTML = `<h4 class="text-sm font-medium text-gray-500">${kpiMapping[key]}</h4><p class="text-3xl font-bold text-gray-800">${value}</p>`;
            kpiGrid.appendChild(card);
        }
    }
    
    function populateTable(tableData = [], allColumns = [], defaultColumns = []) {
        const tableHead = document.querySelector('#data-table thead');
        const tableBody = document.querySelector('#data-table tbody');
        if (!tableHead || !tableBody) return;

        tableHead.innerHTML = '';
        tableBody.innerHTML = '';
        
        const trHead = document.createElement('tr');
        allColumns.forEach(col => {
            const th = document.createElement('th');
            th.className = 'py-2 px-4 border-b text-left sticky top-0 bg-gray-200';
            th.textContent = col;
            if (!defaultColumns.includes(col)) {
                th.style.display = 'none';
            }
            trHead.appendChild(th);
        });
        tableHead.appendChild(trHead);

        tableData.forEach(row => {
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-gray-100';
            allColumns.forEach((col) => {
                const td = document.createElement('td');
                td.className = 'py-2 px-4 border-b';
                
                if (col === 'resume_path' && row[col]) {
                    const link = document.createElement('a');
                    link.href = `/uploads/${row[col]}`;
                    link.textContent = 'View Resume';
                    link.target = '_blank';
                    link.className = 'text-blue-600 hover:underline';
                    td.appendChild(link);
                } else {
                    td.textContent = row[col] || '';
                }

                if (!defaultColumns.includes(col)) {
                    td.style.display = 'none';
                }
                if (col.toLowerCase() === 'name'){ 
                    td.classList.add('font-bold', 'cursor-pointer', 'text-blue-600', 'hover:underline');
                    td.addEventListener('click', () => showDetailsModal(row));      
                }
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });
    }
    
    function populateStatusModal(tableData = []) {
        const modalBody = document.querySelector('#status-modal-body');
        if (!modalBody) return;
        modalBody.innerHTML = '';
        const statuses = ['Applied', 'Shortlisted', 'Interviewed', 'Offered', 'Hired', 'Rejected'];

        const uniqueCandidates = [];
        const seenEmails = new Set();

        tableData.forEach(row => {
            const email = row.email;
            if (email && !seenEmails.has(email.toLowerCase())) {
                seenEmails.add(email.toLowerCase());
                uniqueCandidates.push(row);
            }
        });

        uniqueCandidates.forEach(row => {
            const tr = document.createElement('tr');
            const sanitizedEmail = row.email.replace(/[^a-zA-Z0-9]/g, "");
            const selectId = `status-select-${sanitizedEmail}`;
            let optionsHtml = statuses.map(s => `<option value="${s}" ${row.Status === s ? 'selected' : ''}>${s}</option>`).join('');
            
            tr.innerHTML = `
                <td class="py-2 px-4">${row.name || 'N/A'}</td>
                <td class="py-2 px-4">${row.email}</td>
                <td class="py-2 px-4">
                    <div class="flex items-center">
                        <select id="${selectId}" data-email="${row.email}" data-name="${row.name}" class="status-select border rounded p-1 w-full">${optionsHtml}</select>
                        <span class="feedback-span ml-2 text-sm w-16 text-center"></span>
                    </div>
                </td>
            `;
            modalBody.appendChild(tr);
        });
        
        document.querySelectorAll('.status-select').forEach(select => {
            select.addEventListener('change', handleStatusChange);
        });
    }
    
    function populateColumnSelector(allColumns = [], defaultColumns = []) {
        const optionsContainer = document.getElementById('column-selector-options');
        if (!optionsContainer) return;
        optionsContainer.innerHTML = ''; 

        allColumns.forEach(col => {
            const label = document.createElement('label');
            label.className = 'flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'mr-3 h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500';
            checkbox.value = col;
            checkbox.checked = defaultColumns.includes(col);
            checkbox.addEventListener('change', handleColumnVisibilityChange);

            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(col));
            optionsContainer.appendChild(label);
        });
    }

    function populateFilterOptions(filters = {}) {
        const populate = (id, options, selectedValue) => {
            const select = document.getElementById(id);
            if (!select) return;
            while (select.options.length > 1) select.remove(1);
            options.forEach(opt => select.add(new Option(opt, opt)));
            if (selectedValue) select.value = selectedValue;
            select.dataset.populated = 'true';
        };
        populate('location-filter', filters.locations || []);
        populate('post-filter', filters.posts || []);
        populate('qualification-filter', filters.qualifications || []);
        populate('business-entity-filter', filters.business_entities || []);
        populate('course-filter', filters.courses || []);
        populate('college-filter', filters.colleges || []);
    }
    
    function updateAllCharts(chartData = {}) {
        const chartConfigs = {
            appsPerCompanyChart: { type: 'bar', label: 'Apps per Company', data: chartData.apps_per_company, options: {} },
            appsPerCollegeChart: { type: 'bar', label: 'Apps per College', data: chartData.apps_per_college, options: {} },
            genderDiversityChart: { type: 'pie', label: 'Gender Diversity', data: chartData.gender_diversity, options: {} },
            recruitmentFunnelChart: { type: 'funnel', label: 'Recruitment Funnel', data: chartData.recruitment_funnel, options: {} }
        };

        if (window.ChartDataLabels) {
            Chart.register(window.ChartDataLabels);
        }

        for (const [canvasId, config] of Object.entries(chartConfigs)) {
            const chartInstance = charts[canvasId];
            const data = config.data || {};
            
            if (config.type === 'funnel') {
                const funnelData = chartData.recruitment_funnel || { labels: [], data: [] };
                const funnelLabels = funnelData.labels;
                const funnelValues = funnelData.data;

                const maxValue = Math.max(...funnelValues, 0);
                const spacerData = funnelValues.map(value => (maxValue - value) / 2);

                const newChartData = {
                    labels: funnelLabels,
                    datasets: [{
                        label: 'Spacer',
                        data: spacerData,
                        backgroundColor: 'transparent',
                        stack: 'funnelStack'
                    }, {
                        label: 'Count',
                        data: funnelValues,
                        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
                        stack: 'funnelStack'
                    }]
                };

                if (chartInstance) {
                    chartInstance.destroy();
                }
                const ctx = document.getElementById(canvasId)?.getContext('2d');
                if (!ctx) continue;

                charts[canvasId] = new Chart(ctx, {
                    type: 'bar',
                    data: newChartData,
                    options: {
                        indexAxis: 'y', responsive: true, maintainAspectRatio: false,
                        scales: { x: { stacked: true, grid: { display: false }, ticks: { display: false } }, y: { stacked: true, grid: { display: false } } },
                        plugins: {
                            legend: { display: false }, title: { display: true, text: 'Recruitment Funnel' },
                            tooltip: { filter: (item) => item.datasetIndex === 1 },
                            datalabels: {
                                color: 'white', font: { weight: 'bold', size: 14, },
                                formatter: (value, context) => context.chart.data.datasets[1].data[context.dataIndex],
                                display: (context) => context.datasetIndex === 1
                            }
                        }
                    }
                });

            } else {
                const labels = (config.data && config.data.labels) ? config.data.labels : Object.keys(data);
                const values = (config.data && config.data.data) ? config.data.data : Object.values(data);

                if (chartInstance) {
                    chartInstance.data.labels = labels;
                    chartInstance.data.datasets[0].data = values;
                    chartInstance.update();
                } else {
                    const ctx = document.getElementById(canvasId)?.getContext('2d');
                    if (!ctx) continue;
                    charts[canvasId] = new Chart(ctx, {
                        type: config.type,
                        data: { labels: labels, datasets: [{ label: 'Count', data: values, backgroundColor: config.type === 'pie' ? ['#36A2EB', '#FF6384', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'] : '#36A2EB' }] },
                        options: { ...config.options, responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: config.label } } }
                    });
                }
            }
        }
    }

    // --- UI State Helpers ---
    const showLoading = (isLoading) => document.getElementById('loading-overlay').classList.toggle('hidden', !isLoading);
    const hideError = () => document.getElementById('error-display').classList.add('hidden');
    const showError = (message) => {
        const errorDisplay = document.getElementById('error-display');
        errorDisplay.innerHTML = `<div class="p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">${message}</div>`;
        errorDisplay.classList.remove('hidden');
    };

    // --- Event Handlers ---
    
    function handleColumnVisibilityChange() {
        const selectedColumns = Array.from(document.querySelectorAll('#column-selector-options input:checked')).map(cb => cb.value);
        const table = document.getElementById('data-table');
        if (!table) return;

        table.querySelectorAll('thead th').forEach((th, index) => {
            const isVisible = selectedColumns.includes(th.textContent);
            th.style.display = isVisible ? '' : 'none';
            table.querySelectorAll('tbody tr').forEach(tr => {
                if (tr.children[index]) {
                    tr.children[index].style.display = isVisible ? '' : 'none';
                }
            });
        });
    }

    function showDetailsModal(rowData) {
        const modal = document.getElementById('details-modal');
        const modalBody = modal.querySelector('#modal-body-content');
        if (!modalBody || !modal) return;
        modalBody.innerHTML = '';
        for (const [key, value] of Object.entries(rowData)) {
            if (key === 'resume_path' && value) {
                 modalBody.innerHTML += `<p class="mb-2 text-left"><strong class="text-gray-600">Resume:</strong> <a href="/uploads/${value}" target="_blank" class="text-blue-600 hover:underline">View Resume</a></p>`;
            } else {
                modalBody.innerHTML += `<p class="mb-2 text-left"><strong class="text-gray-600">${key}:</strong> ${value || 'N/A'}</p>`;
            }
        }
        modal.classList.remove('hidden');
    }

    async function handleStatusChange(event) {
        const selectElement = event.target;
        const feedbackSpan = selectElement.parentElement.querySelector('.feedback-span');
        const { email, name } = selectElement.dataset;
        const status = selectElement.value;

        selectElement.disabled = true;
        feedbackSpan.textContent = 'Saving...';
        feedbackSpan.className = 'feedback-span ml-2 text-sm w-16 text-center text-gray-500';

        try {
            const response = await fetch('/api/update_status', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, name, status }),
            });
            if (!response.ok) throw new Error('Server responded with an error.');
            
            feedbackSpan.textContent = 'Saved!';
            feedbackSpan.classList.add('text-green-600');
        } catch (error) {
            feedbackSpan.textContent = 'Error!';
            feedbackSpan.classList.add('text-red-600');
        } finally {
            setTimeout(() => {
                selectElement.disabled = false;
                if(feedbackSpan.textContent !== 'Error!') feedbackSpan.textContent = '';
            }, 2000);
        }
    }

    async function openUserManagementModal() {
        try {
            const response = await fetch('/api/users');
            if (!response.ok) throw new Error('Failed to fetch users.');
            const users = await response.json();
            populateUserList(users);
            document.getElementById('user-management-modal').classList.remove('hidden');
        } catch (error) {
            alert(`Could not load user data: ${error.message}`);
        }
    }

    function populateUserList(users = []) {
        const userListBody = document.getElementById('user-list-body');
        if (!userListBody) return;
        userListBody.innerHTML = '';

        users.forEach(user => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="py-2 px-4">${user.email}</td>
                <td class="py-2 px-4 capitalize">${user.role}</td>
                <td class="py-2 px-4">
                    ${user.role !== 'admin' ? `<button class="delete-user-btn text-red-500 hover:underline text-sm" data-user-id="${user.id}">Delete</button>` : '<span class="text-gray-400 text-sm">Cannot Delete</span>'}
                </td>
            `;
            userListBody.appendChild(tr);
        });

        document.querySelectorAll('.delete-user-btn').forEach(btn => btn.addEventListener('click', handleDeleteUser));
    }

    async function handleAddViewer(event) {
        event.preventDefault();
        const feedbackEl = document.getElementById('add-user-feedback');
        const emailInput = document.getElementById('new-viewer-email');
        const passwordInput = document.getElementById('new-viewer-password');
        
        feedbackEl.textContent = 'Adding...';
        feedbackEl.className = 'text-sm mt-2 text-gray-600';

        try {
            const response = await fetch('/api/users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: emailInput.value, password: passwordInput.value }),
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Failed to add user.');

            feedbackEl.textContent = result.message;
            feedbackEl.classList.add('text-green-600');
            emailInput.value = '';
            passwordInput.value = '';
            openUserManagementModal();
        } catch (error) {
            feedbackEl.textContent = `Error: ${error.message}`;
            feedbackEl.className = 'text-sm mt-2 text-red-600';
        }
    }

    async function handleDeleteUser(event) {
        const userId = event.target.dataset.userId;
        if (!confirm('Are you sure you want to delete this user?')) return;

        try {
            const response = await fetch('/api/users/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: userId }),
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Failed to delete user.');
            openUserManagementModal();
        } catch (error) {
            alert(`Could not delete user: ${error.message}`);
        }
    }

    // --- NEW: Form Configuration Handlers ---

    async function openFormConfigModal() {
        try {
            const response = await fetch('/api/form/config');
            if (!response.ok) throw new Error('Failed to fetch form configuration.');
            const fields = await response.json();
            populateFieldList(fields);
            document.getElementById('form-config-modal').classList.remove('hidden');
        } catch (error) {
            alert(`Could not load form configuration: ${error.message}`);
        }
    }

    function populateFieldList(fields = []) {
        const fieldListBody = document.getElementById('field-list-body');
        if (!fieldListBody) return;
        fieldListBody.innerHTML = '';

        fields.forEach(field => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="py-2 px-4">${field.name}</td>
                <td class="py-2 px-4">${field.label}</td>
                <td class="py-2 px-4 capitalize">${field.type}</td>
                <td class="py-2 px-4">
                    ${!field.is_core ? `<button class="delete-field-btn text-red-500 hover:underline text-sm" data-field-id="${field.id}">Delete</button>` : '<span class="text-gray-400 text-sm">Core Field</span>'}
                </td>
            `;
            fieldListBody.appendChild(tr);
        });

        document.querySelectorAll('.delete-field-btn').forEach(btn => btn.addEventListener('click', handleDeleteField));
    }

    async function handleAddField(event) {
        event.preventDefault();
        const feedbackEl = document.getElementById('add-field-feedback');
        const fieldNameInput = document.getElementById('new-field-name');
        const fieldLabelInput = document.getElementById('new-field-label');
        const fieldTypeInput = document.getElementById('new-field-type');

        const fieldName = fieldNameInput.value.trim().replace(/\s+/g, '_').toLowerCase();
        if (!fieldName) {
            alert('Field Name is required and cannot contain spaces.');
            return;
        }

        feedbackEl.textContent = 'Adding...';
        feedbackEl.className = 'text-sm mt-2 text-gray-600';

        try {
            const response = await fetch('/api/form/config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: fieldName, label: fieldLabelInput.value, type: fieldTypeInput.value }),
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Failed to add field.');
            
            feedbackEl.textContent = result.message;
            feedbackEl.className = 'text-sm mt-2 text-green-600';
            document.getElementById('add-field-form').reset();
            openFormConfigModal(); // Refresh the list
        } catch (error) {
            feedbackEl.textContent = `Error: ${error.message}`;
            feedbackEl.className = 'text-sm mt-2 text-red-600';
        }
    }

    async function handleDeleteField(event) {
        const fieldId = event.target.dataset.fieldId;
        if (!confirm('Are you sure you want to delete this field? This will remove the corresponding column and all its data from the database. This action cannot be undone.')) return;

        try {
            const response = await fetch(`/api/form/config/${fieldId}`, { method: 'DELETE' });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Failed to delete field.');
            openFormConfigModal(); // Refresh the list
        } catch (error) {
            alert(`Could not delete field: ${error.message}`);
        }
    }
    
    function downloadCSV() {
        if (!currentTableData || currentTableData.length === 0) {
            alert("No data available to download.");
            return;
        }

        const selectedColumns = Array.from(document.querySelectorAll('#column-selector-options input:checked')).map(cb => cb.value);
        const headers = selectedColumns.length > 0 ? selectedColumns : Object.keys(currentTableData[0]);
        
        const formatCell = (cell) => {
            let cellString = String(cell === null || cell === undefined ? '' : cell);
            if (cellString.search(/("|,|\n)/g) >= 0) {
                cellString = `"${cellString.replace(/"/g, '""')}"`;
            }
            return cellString;
        };

        const csvContent = [
            headers.join(','),
            ...currentTableData.map(row => headers.map(header => formatCell(row[header])).join(','))
        ].join('\n');
        
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement("a");
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", "recruitment_data.csv");
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    function initializeEventListeners() {
        // --- Modal Handling ---
        const setupModal = (modalId, openBtnId, ...closeBtnIds) => {
            const modal = document.getElementById(modalId);
            const openBtn = document.getElementById(openBtnId);
            if (!modal) return;
            if (openBtn) {
                let openAction = () => modal.classList.remove('hidden');
                if (modalId === 'user-management-modal') openAction = openUserManagementModal;
                if (modalId === 'form-config-modal') openAction = openFormConfigModal;
                openBtn.addEventListener('click', openAction);
            }
            closeBtnIds.forEach(closeBtnId => {
                const closeBtn = document.getElementById(closeBtnId);
                if (closeBtn) {
                    closeBtn.addEventListener('click', () => {
                        modal.classList.add('hidden');
                        if (modalId === 'status-modal' || modalId === 'form-config-modal') {
                            fetchDataAndRender(); // Refresh data on close
                        }
                    });
                }
            });
        };

        setupModal('details-modal', null, 'close-details-modal-btn', 'close-details-modal-btn-2');
        setupModal('status-modal', 'status-management-btn', 'close-status-modal-btn', 'close-status-modal-btn-2');
        setupModal('user-management-modal', 'user-management-btn', 'close-user-modal-btn', 'close-user-modal-btn-2');
        setupModal('form-config-modal', 'form-config-btn', 'close-form-config-modal-btn', 'close-form-config-modal-btn-2');

        // --- Other Event Listeners ---
        document.querySelectorAll('.filter-select').forEach(sel => sel.addEventListener('change', fetchDataAndRender));
        
        document.getElementById('reset-filters-btn').addEventListener('click', () => {
            document.querySelectorAll('.filter-select').forEach(sel => {
                if (sel.type === 'date') sel.value = '';
                else sel.value = 'all';
            });
            fetchDataAndRender();
        });

        document.querySelectorAll('.collapsible-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                this.nextElementSibling.classList.toggle('hidden');
                this.querySelector('svg').classList.toggle('rotate-180');
            });
        });

        document.getElementById('add-viewer-form')?.addEventListener('submit', handleAddViewer);
        document.getElementById('add-field-form')?.addEventListener('submit', handleAddField);

        const columnSelectorBtn = document.getElementById('column-selector-btn');
        const columnSelectorDropdown = document.getElementById('column-selector-dropdown');
        columnSelectorBtn?.addEventListener('click', (e) => {
            e.stopPropagation();
            columnSelectorDropdown.classList.toggle('hidden');
        });
        window.addEventListener('click', () => columnSelectorDropdown?.classList.add('hidden'));

        document.getElementById('download-csv-btn').addEventListener('click', downloadCSV);
    }

    // --- Initial Load ---
    initializeEventListeners();
    fetchDataAndRender();
});
