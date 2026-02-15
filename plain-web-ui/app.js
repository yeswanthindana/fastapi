
async function fetchAPI(url, method = 'GET', body = null) {
    const baseUrl = document.getElementById('baseUrl').value; // Get dynamic URL from input
    const headers = { 'Content-Type': 'application/json' };
    const options = { method, headers };
    if (body) options.body = JSON.stringify(body);

    try {
        const res = await fetch(baseUrl + url, options);
        const data = await res.json();
        return { status: res.status, data };
    } catch (err) {
        return { status: 'Error', data: err.message };
    }
}

// ----------------------------------------------------
// Organizations
// ----------------------------------------------------

async function getAllOrganizations() {
    const { status, data } = await fetchAPI('/organization/all');
    document.getElementById('output-org').innerText = JSON.stringify(data, null, 2);
}

async function createOrganization() {
    const name = document.getElementById('org-name').value;
    const description = document.getElementById('org-desc').value;

    const { status, data } = await fetchAPI('/organization', 'POST', { name, description });
    document.getElementById('output-org').innerText = JSON.stringify(data, null, 2);
}

async function getOrganizationById() {
    const id = document.getElementById('org-id').value;
    if (!id) return alert('Enter Organization ID');
    const { status, data } = await fetchAPI(`/organization/${id}`);
    document.getElementById('output-org').innerText = JSON.stringify(data, null, 2);
}

async function deleteOrganizationById() {
    const id = document.getElementById('org-id').value;
    if (!id) return alert('Enter Organization ID');
    const { status, data } = await fetchAPI(`/organization/${id}`, 'DELETE');
    document.getElementById('output-org').innerText = JSON.stringify(data, null, 2);
}


// ----------------------------------------------------
// Roles
// ----------------------------------------------------

async function getAllRoles() {
    const { status, data } = await fetchAPI('/role/all');
    document.getElementById('output-role').innerText = JSON.stringify(data, null, 2);
}

async function createRole() {
    const name = document.getElementById('role-name').value;
    const description = document.getElementById('role-desc').value;

    const { status, data } = await fetchAPI('/role', 'POST', { name, description });
    document.getElementById('output-role').innerText = JSON.stringify(data, null, 2);
}

async function getRoleById() {
    const id = document.getElementById('role-id').value;
    if (!id) return alert('Enter Role ID');
    const { status, data } = await fetchAPI(`/role/${id}`);
    document.getElementById('output-role').innerText = JSON.stringify(data, null, 2);
}

async function deleteRoleById() {
    const id = document.getElementById('role-id').value;
    if (!id) return alert('Enter Role ID');
    const { status, data } = await fetchAPI(`/role/${id}`, 'DELETE');
    document.getElementById('output-role').innerText = JSON.stringify(data, null, 2);
}


// ----------------------------------------------------
// Users
// ----------------------------------------------------

async function getAllUsers() {
    const { status, data } = await fetchAPI('/user/all');
    document.getElementById('output-user').innerText = JSON.stringify(data, null, 2);
}

async function createUser() {
    const username = document.getElementById('user-username').value;
    const email = document.getElementById('user-email').value;
    const password = document.getElementById('user-password').value;
    const firstname = document.getElementById('user-firstname').value;
    const lastname = document.getElementById('user-lastname').value;
    const role_id = parseInt(document.getElementById('user-role-id').value);
    const organization_id = parseInt(document.getElementById('user-org-id').value);
    const phonenumber = document.getElementById('user-phone').value;

    const body = {
        username, email, password, firstname, lastname, role_id, organization_id, phonenumber
    };

    const { status, data } = await fetchAPI('/user', 'POST', body);
    document.getElementById('output-user').innerText = JSON.stringify(data, null, 2);
}

async function getUserById() {
    const id = document.getElementById('user-id').value;
    if (!id) return alert('Enter User ID');
    const { status, data } = await fetchAPI(`/user/${id}`);
    document.getElementById('output-user').innerText = JSON.stringify(data, null, 2);
}

async function deleteUserById() {
    const id = document.getElementById('user-id').value;
    if (!id) return alert('Enter User ID');
    const { status, data } = await fetchAPI(`/user/${id}`, 'DELETE');
    document.getElementById('output-user').innerText = JSON.stringify(data, null, 2);
}
