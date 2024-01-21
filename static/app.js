document.addEventListener("DOMContentLoaded", function() {
    // Function 1: Handles dynamic form fields based on status
    const statusSelect = document.getElementById('status');
    const programField = document.getElementById('programField');
    const schoolField = document.getElementById('schoolField');
    const departmentField = document.getElementById('departmentField');
    const programSelect = document.getElementById('program');
    const schoolInput = document.getElementById('school');
    const departmentSelect = document.getElementById('department');

    statusSelect.addEventListener('change', function() {
        const selectedValue = statusSelect.value;

        if (selectedValue === 'Student') {
            departmentField.style.display = 'none';
            programField.style.display = 'block';
            schoolField.style.display = 'block';

            programSelect.setAttribute('required', 'required');
            schoolInput.setAttribute('required', 'required');
            departmentSelect.removeAttribute('required');
        } else if (selectedValue === 'Teaching staff' || selectedValue === 'Non-teaching staff') {
            programField.style.display = 'none';
            schoolField.style.display = 'none';
            departmentField.style.display = 'block';

            departmentSelect.setAttribute('required', 'required');
            programSelect.removeAttribute('required');
            schoolInput.removeAttribute('required');
        } else {
            programField.style.display = 'block';
            schoolField.style.display = 'block';
            departmentField.style.display = 'block';

            programSelect.setAttribute('required', 'required');
            schoolInput.setAttribute('required', 'required');
            departmentSelect.setAttribute('required', 'required');
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Function 2: Handles password section visibility
    const changePasswordCheckbox = document.getElementById('changePassword');
    const passwordSection = document.getElementById('passwordSection');

    changePasswordCheckbox.addEventListener('change', function () {
        passwordSection.style.display = changePasswordCheckbox.checked ? 'block' : 'none';
    });
});


