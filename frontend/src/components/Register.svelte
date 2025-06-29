<script>
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher();
  
  let username = '';
  let email = '';
  let password = '';
  let confirmPassword = '';
  let userInfo = '';
  let companyDeptClub = '';
  let error = '';
  let success = '';
  let loading = false;

  async function handleRegister() {
    if (!username || !email || !password || !confirmPassword) {
      error = 'すべての必須項目を入力してください';
      return;
    }

    if (password !== confirmPassword) {
      error = 'パスワードが一致しません';
      return;
    }

    if (password.length < 6) {
      error = 'パスワードは6文字以上で入力してください';
      return;
    }

    loading = true;
    error = '';
    success = '';

    try {
      console.log('Attempting registration with username:', username);
      
      const response = await fetch('http://localhost:5000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          username, 
          email, 
          password,
          user_info: userInfo,
          company_dept_club: companyDeptClub
        }),
      });

      console.log('Registration response status:', response.status);
      const data = await response.json();
      console.log('Registration response data:', data);

      if (response.ok) {
        success = '登録が完了しました！ログインページに移動します...';
        // フォームをクリア
        username = '';
        email = '';
        password = '';
        confirmPassword = '';
        userInfo = '';
        companyDeptClub = '';
        
        setTimeout(() => {
          showLogin();
        }, 2000);
      } else {
        error = data.error || '登録に失敗しました';
      }
    } catch (err) {
      console.error('Registration error:', err);
      error = 'サーバーへの接続に失敗しました';
    } finally {
      loading = false;
    }
  }

  function showLogin() {
    dispatch('showLogin');
  }

  function handleKeyPress(event) {
    if (event.key === 'Enter') {
      handleRegister();
    }
  }

  function clearMessages() {
    error = '';
    success = '';
  }
</script>

<div class="register-container">
  <h2>新規登録</h2>
  
  {#if error}
    <div class="message error">{error}</div>
  {/if}

  {#if success}
    <div class="message success">{success}</div>
  {/if}

  <form on:submit|preventDefault={handleRegister}>
    <div class="form-group">
      <label for="username">ユーザー名 <span class="required">*</span></label>
      <input
        id="username"
        type="text"
        bind:value={username}
        disabled={loading}
        on:keypress={handleKeyPress}
        on:focus={clearMessages}
        placeholder="ユーザー名を入力"
        required
      />
    </div>

    <div class="form-group">
      <label for="email">メールアドレス <span class="required">*</span></label>
      <input
        id="email"
        type="email"
        bind:value={email}
        disabled={loading}
        on:keypress={handleKeyPress}
        on:focus={clearMessages}
        placeholder="example@email.com"
        required
      />
    </div>

    <div class="form-group">
      <label for="company">会社・組織・クラブ</label>
      <input
        id="company"
        type="text"
        bind:value={companyDeptClub}
        disabled={loading}
        on:keypress={handleKeyPress}
        on:focus={clearMessages}
        placeholder="所属する会社や組織、クラブ名"
      />
    </div>

    <div class="form-group">
      <label for="userInfo">ユーザー情報</label>
      <textarea
        id="userInfo"
        bind:value={userInfo}
        disabled={loading}
        on:focus={clearMessages}
        placeholder="自己紹介や追加情報があれば入力してください"
        rows="3"
      ></textarea>
    </div>

    <div class="form-group">
      <label for="password">パスワード <span class="required">*</span></label>
      <input
        id="password"
        type="password"
        bind:value={password}
        disabled={loading}
        on:keypress={handleKeyPress}
        on:focus={clearMessages}
        placeholder="6文字以上のパスワード"
        required
      />
    </div>

    <div class="form-group">
      <label for="confirmPassword">パスワード確認 <span class="required">*</span></label>
      <input
        id="confirmPassword"
        type="password"
        bind:value={confirmPassword}
        disabled={loading}
        on:keypress={handleKeyPress}
        on:focus={clearMessages}
        placeholder="上記のパスワードを再入力"
        required
      />
    </div>

    <button type="submit" disabled={loading}>
      {loading ? '登録中...' : '新規登録'}
    </button>
  </form>

  <p class="login-link">
    すでにアカウントをお持ちの方は
    <button class="link-button" on:click={showLogin} disabled={loading}>ログイン</button>
  </p>
</div>

<style>
  .register-container {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
  }

  h2 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
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

  .form-group {
    margin-bottom: 20px;
  }

  label {
    display: block;
    margin-bottom: 6px;
    font-weight: bold;
    color: #495057;
  }

  .required {
    color: #dc3545;
  }

  input,
  textarea {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 16px;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  }

  input:focus,
  textarea:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  }

  input:disabled,
  textarea:disabled {
    background-color: #e9ecef;
    opacity: 1;
  }

  textarea {
    resize: vertical;
    min-height: 80px;
  }

  button[type="submit"] {
    width: 100%;
    padding: 12px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.15s ease-in-out;
  }

  button[type="submit"]:hover:not(:disabled) {
    background-color: #218838;
  }

  button[type="submit"]:disabled {
    background-color: #6c757d;
    cursor: not-allowed;
  }

  .login-link {
    text-align: center;
    margin-top: 30px;
    color: #6c757d;
  }

  .link-button {
    background: none;
    color: #007bff;
    border: none;
    cursor: pointer;
    text-decoration: underline;
    font-size: inherit;
    padding: 0;
  }

  .link-button:hover:not(:disabled) {
    color: #0056b3;
  }

  .link-button:disabled {
    color: #6c757d;
    cursor: not-allowed;
    text-decoration: none;
  }

  @media (max-width: 576px) {
    .register-container {
      padding: 15px;
    }

    input,
    textarea {
      font-size: 16px; /* Prevent zoom on iOS */
    }
  }
</style>