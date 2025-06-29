<style>
  .dashboard {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid #eee;
  }

  .user-info h2 {
    margin: 0;
    color: #333;
  }

  .user-info p {
    margin: 5px 0;
    color: #666;
  }

  .company {
    font-style: italic;
    color: #888;
  }

  .logout-btn {
    background-color: #dc3545;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
  }

  .logout-btn:hover {
    background-color: #c82333;
  }

  .message {
    padding: 12px;
    border-radius: 4px;
    margin-bottom: 20px;
  }

  .message.success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
  }

  .message.error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }

  section {
    margin-bottom: 40px;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #e9ecef;
  }

  h3 {
    margin-top: 0;
    color: #495057;
    border-bottom: 2px solid #007bff;
    padding-bottom: 10px;
  }

  h4 {
    color: #6c757d;
    margin-bottom: 15px;
  }

  .init-section {
    background-color: #fff3cd;
    border-color: #ffeaa7;
  }

  .init-btn {
    background-color: #ffc107;
    color: #212529;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
  }

  .init-btn:hover {
    background-color: #e0a800;
  }

  .warning {
    margin-top: 10px;
    color: #856404;
    font-size: 14px;
    font-style: italic;
  }

  .form-row {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    gap: 10px;
  }

  .form-row label {
    min-width: 80px;
    font-weight: bold;
    color: #495057;
  }

  .form-row input,
  .form-row select,
  .form-row textarea {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 14px;
  }

  .form-row textarea {
    min-height: 80px;
    resize: vertical;
  }

  .form-row button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    white-space: nowrap;
  }

  .form-row button:hover {
    background-color: #0056b3;
  }

  .subjects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 15px;
    margin-top: 15px;
  }

  .subject-card {
    background-color: white;
    padding: 15px;
    border-radius: 6px;
    border: 1px solid #dee2e6;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .subject-card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transform: translateY(-2px);
    border-color: #007bff;
  }

  .clickable-title {
    margin: 0 0 8px 0;
    color: #007bff;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .click-hint {
    font-size: 12px;
    color: #6c757d;
    font-weight: normal;
  }

  .subject-card p.time {
    margin: 0 0 8px 0;
    color: #6c757d;
    font-size: 14px;
    font-weight: 500;
  }

  .subject-card p.teacher {
    margin: 0 0 5px 0;
    color: #28a745;
    font-size: 13px;
  }

  .subject-card p.department {
    margin: 0 0 8px 0;
    color: #17a2b8;
    font-size: 13px;
  }

  .subject-card p.description {
    margin: 0;
    color: #868e96;
    font-size: 12px;
    font-style: italic;
    line-height: 1.4;
  }

  .import-section {
    background-color: #e3f2fd;
    border: 1px solid #bbdefb;
    border-radius: 6px;
    padding: 20px;
    margin-bottom: 20px;
  }

  .import-controls {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 15px;
    flex-wrap: wrap;
  }

  .file-select-btn {
    background-color: #2196f3;
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
  }

  .file-select-btn:hover {
    background-color: #1976d2;
  }

  .import-btn {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
  }

  .import-btn:hover:not(:disabled) {
    background-color: #45a049;
  }

  .import-btn:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }

  .template-btn {
    background-color: #ff9800;
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
  }

  .template-btn:hover {
    background-color: #f57c00;
  }

  .file-info {
    color: #1976d2;
    font-size: 14px;
    font-weight: 500;
  }

  .import-info {
    background-color: #f8f9fa;
    border-radius: 4px;
    padding: 15px;
  }

  .import-info ul {
    margin: 10px 0 0 20px;
    color: #6c757d;
  }

  .import-info li {
    margin-bottom: 5px;
  }

  .qr-result {
    margin-top: 20px;
    text-align: center;
    background-color: white;
    padding: 20px;
    border-radius: 6px;
    border: 1px solid #dee2e6;
  }

  .qr-result img {
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .table-container {
    background-color: white;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid #dee2e6;
  }

  table {
    width: 100%;
    border-collapse: collapse;
  }

  th,
  td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #dee2e6;
  }

  th {
    background-color: #f8f9fa;
    font-weight: bold;
    color: #495057;
  }

  tr:hover {
    background-color: #f5f5f5;
  }

  .status-出勤 {
    color: #28a745;
    font-weight: bold;
  }

  .status-欠勤 {
    color: #dc3545;
    font-weight: bold;
  }

  .status-遅刻 {
    color: #ffc107;
    font-weight: bold;
  }

  .status-早退 {
    color: #fd7e14;
    font-weight: bold;
  }

  .history-tabs {
    margin-top: 20px;
  }

  .tab-content {
    margin-bottom: 30px;
  }

  /* モーダルスタイル */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal-content {
    background-color: white;
    border-radius: 8px;
    max-width: 800px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    width: 90%;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid #dee2e6;
    background-color: #f8f9fa;
    border-radius: 8px 8px 0 0;
  }

  .modal-header h3 {
    margin: 0;
    color: #495057;
    border: none;
    padding: 0;
  }

  .close-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #6c757d;
    padding: 0;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .close-btn:hover {
    color: #495057;
  }

  .modal-body {
    padding: 20px;
  }

  .subject-details {
    space-y: 20px;
  }

  .detail-group {
    margin-bottom: 25px;
  }

  .detail-group h4 {
    color: #007bff;
    border-bottom: 1px solid #dee2e6;
    padding-bottom: 8px;
    margin-bottom: 15px;
  }

  .detail-item {
    margin-bottom: 10px;
    padding: 8px 0;
    border-bottom: 1px solid #f8f9fa;
  }

  .detail-item strong {
    color: #495057;
    margin-right: 10px;
    min-width: 100px;
    display: inline-block;
  }

  .schedule-table {
    margin-top: 10px;
  }

  .schedule-table table {
    background-color: #f8f9fa;
    border-radius: 4px;
  }

  .schedule-table th {
    background-color: #e9ecef;
  }

  .excel-data {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    padding: 15px;
    max-height: 300px;
    overflow-y: auto;
  }

  .excel-data pre {
    margin: 0;
    white-space: pre-wrap;
    word-break: break-word;
    font-size: 12px;
    line-height: 1.4;
    color: #495057;
  }

  @media (max-width: 768px) {
    .dashboard {
      padding: 10px;
    }

    header {
      flex-direction: column;
      align-items: flex-start;
      gap: 10px;
    }

    .form-row {
      flex-direction: column;
      align-items: flex-start;
    }

    .form-row label {
      min-width: auto;
      margin-bottom: 5px;
    }

    .subjects-grid {
      grid-template-columns: 1fr;
    }
    
    .table-container {
      overflow-x: auto;
    }

    .modal-content {
      width: 95%;
      max-width: none;
    }

    .modal-header {
      padding: 15px;
    }

    .modal-body {
      padding: 15px;
    }

    .click-hint {
      display: none;
    }
  }
</style><script>
  import { createEventDispatcher, onMount } from 'svelte';
  
  const dispatch = createEventDispatcher();
  
  export let user;
  export let token;
  
  let qrCode = '';
  let qrData = '';
  let selectedDate = new Date().toISOString().split('T')[0];
  let attendances = [];
  let subjects = [];
  let exceptions = [];
  let message = '';
  let error = '';
  
  // フォーム用の変数
  let selectedSubjectId = '';
  let attendanceStatus = '出勤';
  let attendanceTime = '';
  let exceptionReason = '';
  let exceptionNotes = '';
  let exceptionDate = new Date().toISOString().split('T')[0];
  
  // 新しい科目追加用
  let newSubjectName = '';
  let newSubjectTime = '';
  
  // エクセルインポート用
  let fileInput;
  let selectedFile = null;
  let importing = false;

  // 科目詳細表示用
  let selectedSubjectDetail = null;
  let showSubjectModal = false;

  onMount(() => {
    loadSubjects();
    loadAttendance();
    loadExceptions();
  });

  async function initDatabase() {
    try {
      const response = await fetch('http://localhost:5000/api/init-db', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();

      if (response.ok) {
        message = 'データベースが初期化されました';
        await loadSubjects();
        await loadAttendance();
        await loadExceptions();
      } else {
        error = data.error || 'データベース初期化に失敗しました';
      }
    } catch (err) {
      console.error('Database init error:', err);
      error = `接続に失敗しました: ${err.message}`;
    }
  }

  async function loadSubjects() {
    try {
      const response = await fetch('http://localhost:5000/api/subjects', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        subjects = await response.json();
      } else if (response.status === 401) {
        logout();
      } else {
        console.error('Failed to load subjects:', response.status);
      }
    } catch (err) {
      console.error('Failed to load subjects:', err);
    }
  }

  async function createSubject() {
    if (!newSubjectName) {
      error = '科目名を入力してください';
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/subjects', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          name: newSubjectName,
          attendance_time: newSubjectTime
        })
      });

      const data = await response.json();

      if (response.ok) {
        message = '科目が追加されました';
        newSubjectName = '';
        newSubjectTime = '';
        loadSubjects();
      } else {
        error = data.error || '科目の追加に失敗しました';
      }
    } catch (err) {
      console.error('Create subject error:', err);
      error = `接続に失敗しました: ${err.message}`;
    }
  }

  async function showSubjectDetail(subjectId) {
    try {
      const response = await fetch(`http://localhost:5000/api/subjects/${subjectId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        selectedSubjectDetail = await response.json();
        showSubjectModal = true;
      } else {
        error = '科目詳細の取得に失敗しました';
      }
    } catch (err) {
      console.error('Subject detail error:', err);
      error = `科目詳細の取得に失敗しました: ${err.message}`;
    }
  }

  function closeSubjectModal() {
    showSubjectModal = false;
    selectedSubjectDetail = null;
  }

  function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
      selectedFile = file;
      clearMessages();
    }
  }

  async function importExcelFile() {
    if (!selectedFile) {
      error = 'ファイルを選択してください';
      return;
    }

    importing = true;
    error = '';
    message = '';

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:5000/api/import-excel', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      const data = await response.json();

      if (response.ok) {
        message = `インポート完了: ${data.subjects_created}個の科目、${data.schedules_created}個のスケジュールを処理しました`;
        selectedFile = null;
        fileInput.value = '';
        loadSubjects();
      } else {
        error = data.error || 'インポートに失敗しました';
      }
    } catch (err) {
      console.error('Import error:', err);
      error = `インポートに失敗しました: ${err.message}`;
    } finally {
      importing = false;
    }
  }

  async function downloadTemplate() {
    try {
      const response = await fetch('http://localhost:5000/api/download-template', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'attendance_template.xlsx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        message = 'テンプレートファイルをダウンロードしました';
      } else {
        error = 'テンプレートダウンロードに失敗しました';
      }
    } catch (err) {
      console.error('Template download error:', err);
      error = `ダウンロードに失敗しました: ${err.message}`;
    }
  }

  async function recordAttendance() {
    if (!selectedSubjectId) {
      error = '科目を選択してください';
      return;
    }

    error = '';
    message = '';
    
    try {
      const response = await fetch('http://localhost:5000/api/attendance', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          subject_id: selectedSubjectId,
          date: selectedDate,
          status: attendanceStatus,
          time: attendanceTime
        })
      });

      const data = await response.json();

      if (response.ok) {
        message = '出勤記録が保存されました';
        selectedSubjectId = '';
        attendanceTime = '';
        loadAttendance();
      } else if (response.status === 401) {
        error = 'セッションが期限切れです。再ログインしてください。';
        setTimeout(() => {
          logout();
        }, 2000);
      } else {
        error = data.error || '出勤記録の保存に失敗しました';
      }
    } catch (err) {
      console.error('Record attendance error:', err);
      error = `接続に失敗しました: ${err.message}`;
    }
  }

  async function loadAttendance() {
    try {
      const response = await fetch('http://localhost:5000/api/attendance', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        attendances = await response.json();
      } else if (response.status === 401) {
        logout();
      } else {
        console.error('Failed to load attendance:', response.status);
      }
    } catch (err) {
      console.error('Failed to load attendance:', err);
    }
  }

  async function createException() {
    if (!exceptionReason) {
      error = '理由を入力してください';
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/exceptions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          date: exceptionDate,
          reason: exceptionReason,
          notes: exceptionNotes
        })
      });

      const data = await response.json();

      if (response.ok) {
        message = '例外記録が保存されました';
        exceptionReason = '';
        exceptionNotes = '';
        exceptionDate = new Date().toISOString().split('T')[0];
        loadExceptions();
      } else {
        error = data.error || '例外記録の保存に失敗しました';
      }
    } catch (err) {
      console.error('Create exception error:', err);
      error = `接続に失敗しました: ${err.message}`;
    }
  }

  async function loadExceptions() {
    try {
      const response = await fetch('http://localhost:5000/api/exceptions', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        exceptions = await response.json();
      } else if (response.status === 401) {
        logout();
      } else {
        console.error('Failed to load exceptions:', response.status);
      }
    } catch (err) {
      console.error('Failed to load exceptions:', err);
    }
  }

  async function generateQR() {
    error = '';
    message = '';
    
    try {
      const response = await fetch('http://localhost:5000/api/generate-qr', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ date: selectedDate }),
      });

      const data = await response.json();

      if (response.ok) {
        qrCode = data.qr_code;
        qrData = data.data;
        message = 'QRコードが生成されました';
      } else if (response.status === 401) {
        error = 'セッションが期限切れです。再ログインしてください。';
        setTimeout(() => {
          logout();
        }, 2000);
      } else {
        error = data.error || 'QRコードの生成に失敗しました';
      }
    } catch (err) {
      console.error('QR generation error:', err);
      error = `接続に失敗しました: ${err.message}`;
    }
  }

  function logout() {
    dispatch('logout');
  }

  function clearMessages() {
    message = '';
    error = '';
  }

  function formatExcelData(excelDataStr) {
    try {
      // 文字列をオブジェクトに変換
      const excelData = eval('(' + excelDataStr + ')');
      return excelData;
    } catch (e) {
      return null;
    }
  }
</script>

<div class="dashboard">
  <header>
    <h2>ダッシュボード</h2>
    <div class="user-info">
      <p>ようこそ、{user.username}さん</p>
      {#if user.company_dept_club}
        <p class="company">{user.company_dept_club}</p>
      {/if}
    </div>
    <button class="logout-btn" on:click={logout}>ログアウト</button>
  </header>
  
  {#if message}
    <div class="message success">{message}</div>
  {/if}
  
  {#if error}
    <div class="message error">{error}</div>
  {/if}

  <section class="init-section">
    <h3>データベース管理</h3>
    <button class="init-btn" on:click={initDatabase}>データベースを初期化</button>
    <p class="warning">※ 既存のデータがすべて削除され、新しいデータベース構造で再作成されます</p>
  </section>

  <section class="subjects-section">
    <h3>科目管理</h3>
    
    <div class="import-section">
      <h4>エクセルファイルから科目をインポート</h4>
      <div class="import-controls">
        <input
          type="file"
          accept=".xlsx,.xls"
          bind:this={fileInput}
          on:change={handleFileSelect}
          style="display: none;"
        />
        <button class="file-select-btn" on:click={() => fileInput.click()}>
          📁 エクセルファイルを選択
        </button>
        
        {#if selectedFile}
          <span class="file-info">選択されたファイル: {selectedFile.name}</span>
          <button class="import-btn" on:click={importExcelFile} disabled={importing}>
            {importing ? 'インポート中...' : '📊 インポート実行'}
          </button>
        {/if}
        
        <button class="template-btn" on:click={downloadTemplate}>
          📄 テンプレートダウンロード
        </button>
      </div>
      
      <div class="import-info">
        <p><strong>インポート対象:</strong></p>
        <ul>
          <li>Sheet1: 科目基本情報（科目名、授業時間、担当者など）</li>
          <li>Sheet2: 出勤スケジュール（出講日、時間数など）</li>
        </ul>
      </div>
    </div>
    
    <div class="add-subject">
      <h4>新しい科目を手動追加</h4>
      <div class="form-row">
        <input
          type="text"
          bind:value={newSubjectName}
          placeholder="科目名"
          on:focus={clearMessages}
        />
        <input
          type="text"
          bind:value={newSubjectTime}
          placeholder="授業時間 (例: 9:00-10:30)"
          on:focus={clearMessages}
        />
        <button on:click={createSubject}>追加</button>
      </div>
    </div>

    <div class="subjects-list">
      <h4>登録済み科目</h4>
      {#if subjects.length > 0}
        <div class="subjects-grid">
          {#each subjects as subject}
            <div class="subject-card" on:click={() => showSubjectDetail(subject.id)}>
              <h5 class="clickable-title">
                {subject.name}
                <span class="click-hint">👁️ 詳細を見る</span>
              </h5>
              <p class="time">{subject.attendance_time}</p>
              {#if subject.teacher_name}
                <p class="teacher">担当: {subject.teacher_name}</p>
              {/if}
              {#if subject.department}
                <p class="department">所属: {subject.department}</p>
              {/if}
              {#if subject.description}
                <p class="description">{subject.description}</p>
              {/if}
            </div>
          {/each}
        </div>
      {:else}
        <p>科目が登録されていません</p>
      {/if}
    </div>
  </section>

  <section class="attendance-section">
    <h3>出勤記録</h3>
    
    <div class="record-attendance">
      <div class="form-row">
        <label for="date">日付:</label>
        <input
          id="date"
          type="date"
          bind:value={selectedDate}
          on:focus={clearMessages}
        />
      </div>
      
      <div class="form-row">
        <label for="subject">科目:</label>
        <select id="subject" bind:value={selectedSubjectId} on:focus={clearMessages}>
          <option value="">科目を選択してください</option>
          {#each subjects as subject}
            <option value={subject.id}>{subject.name}</option>
          {/each}
        </select>
      </div>
      
      <div class="form-row">
        <label for="status">出勤状況:</label>
        <select id="status" bind:value={attendanceStatus}>
          <option value="出勤">出勤</option>
          <option value="欠勤">欠勤</option>
          <option value="遅刻">遅刻</option>
          <option value="早退">早退</option>
        </select>
      </div>
      
      <div class="form-row">
        <label for="time">時間:</label>
        <input
          id="time"
          type="text"
          bind:value={attendanceTime}
          placeholder="例: 9:15-10:30"
          on:focus={clearMessages}
        />
      </div>
      
      <button on:click={recordAttendance}>出勤記録を保存</button>
    </div>
  </section>

  <section class="exception-section">
    <h3>例外記録</h3>
    
    <div class="record-exception">
      <div class="form-row">
        <label for="exception-date">日付:</label>
        <input
          id="exception-date"
          type="date"
          bind:value={exceptionDate}
          on:focus={clearMessages}
        />
      </div>
      
      <div class="form-row">
        <label for="reason">理由:</label>
        <input
          id="reason"
          type="text"
          bind:value={exceptionReason}
          placeholder="理由を入力してください"
          on:focus={clearMessages}
        />
      </div>
      
      <div class="form-row">
        <label for="notes">備考:</label>
        <textarea
          id="notes"
          bind:value={exceptionNotes}
          placeholder="詳細な説明があれば入力してください"
          on:focus={clearMessages}
        ></textarea>
      </div>
      
      <button on:click={createException}>例外記録を保存</button>
    </div>
  </section>

  <section class="qr-section">
    <h3>QRコード生成</h3>
    <div class="qr-generator">
      <div class="form-row">
        <label for="qr-date">日付:</label>
        <input
          id="qr-date"
          type="date"
          bind:value={selectedDate}
          on:focus={clearMessages}
        />
        <button on:click={generateQR}>QRコード生成</button>
      </div>
      
      {#if qrCode}
        <div class="qr-result">
          <h4>生成されたQRコード</h4>
          <img src={qrCode} alt="QR Code" />
          <p>データ: {qrData}</p>
        </div>
      {/if}
    </div>
  </section>

  <section class="history-section">
    <h3>履歴</h3>
    
    <div class="history-tabs">
      <div class="tab-content">
        <h4>出勤履歴</h4>
        {#if attendances.length > 0}
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>日付</th>
                  <th>科目</th>
                  <th>出勤状況</th>
                  <th>時間</th>
                </tr>
              </thead>
              <tbody>
                {#each attendances as attendance}
                  <tr>
                    <td>{attendance.date}</td>
                    <td>{attendance.subject_name}</td>
                    <td class="status-{attendance.status}">{attendance.status}</td>
                    <td>{attendance.time || '-'}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        {:else}
          <p>出勤履歴がありません</p>
        {/if}
      </div>
      
      <div class="tab-content">
        <h4>例外履歴</h4>
        {#if exceptions.length > 0}
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>日付</th>
                  <th>理由</th>
                  <th>備考</th>
                </tr>
              </thead>
              <tbody>
                {#each exceptions as exception}
                  <tr>
                    <td>{exception.date}</td>
                    <td>{exception.reason}</td>
                    <td>{exception.notes || '-'}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        {:else}
          <p>例外履歴がありません</p>
        {/if}
      </div>
    </div>
  </section>
</div>

<!-- 科目詳細モーダル -->
{#if showSubjectModal && selectedSubjectDetail}
  <div class="modal-overlay" on:click={closeSubjectModal}>
    <div class="modal-content" on:click|stopPropagation>
      <div class="modal-header">
        <h3>{selectedSubjectDetail.name} - 詳細情報</h3>
        <button class="close-btn" on:click={closeSubjectModal}>×</button>
      </div>
      
      <div class="modal-body">
        <div class="subject-details">
          <div class="detail-group">
            <h4>基本情報</h4>
            <div class="detail-item">
              <strong>科目名:</strong> {selectedSubjectDetail.name}
            </div>
            {#if selectedSubjectDetail.teacher_name}
              <div class="detail-item">
                <strong>担当者:</strong> {selectedSubjectDetail.teacher_name}
              </div>
            {/if}
            {#if selectedSubjectDetail.department}
              <div class="detail-item">
                <strong>所属:</strong> {selectedSubjectDetail.department}
              </div>
            {/if}
            {#if selectedSubjectDetail.attendance_time}
              <div class="detail-item">
                <strong>授業時間:</strong> {selectedSubjectDetail.attendance_time}
              </div>
            {/if}
            {#if selectedSubjectDetail.credits}
              <div class="detail-item">
                <strong>単位数:</strong> {selectedSubjectDetail.credits}
              </div>
            {/if}
            {#if selectedSubjectDetail.description}
              <div class="detail-item">
                <strong>説明:</strong> {selectedSubjectDetail.description}
              </div>
            {/if}
          </div>

          {#if selectedSubjectDetail.schedules && selectedSubjectDetail.schedules.length > 0}
            <div class="detail-group">
              <h4>スケジュール</h4>
              <div class="schedule-table">
                <table>
                  <thead>
                    <tr>
                      <th>日付</th>
                      <th>時間数</th>
                      <th>場所</th>
                      <th>備考</th>
                    </tr>
                  </thead>
                  <tbody>
                    {#each selectedSubjectDetail.schedules as schedule}
                      <tr>
                        <td>{schedule.date || '-'}</td>
                        <td>{schedule.hours || '-'}</td>
                        <td>{schedule.location || '-'}</td>
                        <td>{schedule.notes || '-'}</td>
                      </tr>
                    {/each}
                  </tbody>
                </table>
              </div>
            </div>
          {/if}

          {#if selectedSubjectDetail.excel_data}
            <div class="detail-group">
              <h4>インポートされたエクセルデータ</h4>
              <div class="excel-data">
                <pre>{selectedSubjectDetail.excel_data}</pre>
              </div>
            </div>
          {/if}
        </div>
      </div>
    </div>
  </div>
{/if}