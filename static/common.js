// 后端基础地址
const BASE_URL = "http://127.0.0.1:8000/api";

// 获取请求头（自动带Token）
function getHeaders() {
    return {
        'Authorization': 'Bearer ' + localStorage.getItem('token'),
        'Content-Type': 'application/json'
    };
}

// 登录校验（所有后台页面必须加载）
function checkLogin() {
    const token = localStorage.getItem('token');
    const path = window.location.pathname;
    if (!token && !path.includes('login') && !path.includes('register')) {
        window.location.href = 'login.html';
    }
}

// 统一请求方法
async function request(url, method = 'GET', data = {}) {
    try {
        const opts = { method, headers: getHeaders() };
        if (method !== 'GET') opts.body = JSON.stringify(data);
        const res = await fetch(BASE_URL + url, opts);
        return await res.json();
    } catch (e) {
        alert('请求失败：' + e.message);
        return null;
    }
}

// 图片上传专用请求
async function uploadRequest(url, formData) {
    try {
        const res = await fetch(BASE_URL + url, {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') },
            body: formData
        });
        return await res.json();
    } catch (e) {
        alert('上传失败：' + e.message);
        return null;
    }
}

// 退出登录
function logout() {
    localStorage.clear();
    alert('已退出登录');
    window.location.href = 'login.html';
}

// 提示框
function showMsg(msg) {
    alert(msg);
    window.location.reload();
}