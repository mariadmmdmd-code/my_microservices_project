async function validateForm(event) {
    event.preventDefault();
    
    const formData = new FormData();
    formData.append('first_name', document.getElementById('firstName').value);
    formData.append('last_name', document.getElementById('lastName').value);
    formData.append('age', document.getElementById('age').value);
    formData.append('email', document.getElementById('email').value);
    formData.append('favorite_album', document.getElementById('album').value);
    formData.append('password', document.getElementById('password').value);
    formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
    
    const resultDiv = document.getElementById('validationResult');
    
    try {
        const response = await fetch('login/js/', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.style.backgroundColor = '#d4edda';
            resultDiv.style.color = '#155724';
            resultDiv.innerHTML = data.message;
            setTimeout(() => {
                window.location.href = 'login/css/';
            }, 1500);
        } else {
            resultDiv.style.backgroundColor = '#f8d7da';
            resultDiv.style.color = '#721c24';
            let errorHtml = '';
            for (const [field, errors] of Object.entries(data.errors)) {
                errorHtml += `<p>${field}: ${errors.join(', ')}</p>`;
                const input = document.getElementById(field === 'first_name' ? 'firstName' : 
                                                       field === 'last_name' ? 'lastName' :
                                                       field === 'age' ? 'age' :
                                                       field === 'email' ? 'email' : null);
                if (input) input.style.borderColor = 'red';
            }
            resultDiv.innerHTML = errorHtml;
        }
    } catch (error) {
        resultDiv.style.backgroundColor = '#f8d7da';
        resultDiv.style.color = '#721c24';
        resultDiv.innerHTML = 'Server error. Please try again.';
    }
    
    return false;
}