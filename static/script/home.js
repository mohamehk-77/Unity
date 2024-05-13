document.addEventListener("DOMContentLoaded", function() {
    // Define global variables
    const Settings = document.querySelector('#Settings');
    const settingModal = document.querySelector('.Settings');

    const menuItems = document.querySelectorAll('.MenuItems');
    const MessagesBox = document.getElementById('MessagesHightlight');
    const MessagesLink = document.getElementById('MessagesNoti');
    const Messages = document.querySelector('.Messages');
    const Message = Messages.querySelectorAll('.Message');
    const MessageSearch = document.querySelector("#MessageSearch");
    const Theme = document.querySelector('#Thme');
    const ThemeModal = document.querySelector('.Theme');
    const fontSize = document.querySelectorAll('.ChooseSize span');
    var root  = document.querySelector(':root');
    const colorPalette = document.querySelectorAll('.ChooseColor span');
    const BG1 = document.querySelector('.BG-1');
    const BG2 = document.querySelector('.BG-2');
    const BG3 = document.querySelector('.BG-3');
    
    const changeActItem = () => {
        menuItems.forEach(item => {
            item.classList.remove('ACT');
        });
    };

    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            changeActItem();
            item.classList.add('ACT');
            if (item.id !== 'Noti') {
                document.querySelector('.NotiPopup').style.display = 'none';
            } else {
                document.querySelector('.NotiPopup').style.display = 'block';
                item.querySelector('.NotiCount').style.display = 'none';
            }
        });
    });

    const SearchMessage = () => {
        const val = MessageSearch.value.toLowerCase();
        console.log(val);
        Message.forEach(chat => {
            let name = chat.querySelector('h5').textContent.toLowerCase();
            if (name.indexOf(val) !== -1) {
                chat.style.display = 'flex';
            } else {
                chat.style.display = 'none';
            }
        });
    };

    MessageSearch.addEventListener('keyup', SearchMessage);

    MessagesLink.addEventListener('click', () => {
        MessagesBox.classList.toggle('MessageHighlight');
    });

    const handleClickOutsideMessage = (event) => {
        if (!MessagesBox.contains(event.target) && !MessagesLink.contains(event.target)) {
            MessagesBox.classList.remove('MessageHighlight');
        }
    };

    document.body.addEventListener('click', handleClickOutsideMessage);

    // Event listener for theme button
    Theme.addEventListener('click', () => {
        ThemeModal.style.display = 'grid';
    });

    // Event listener to close theme modal
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('Theme')) {
            ThemeModal.style.display = 'none';
        }
    });
    const removeSelector = () => {
        fontSize.forEach(size => {
            size.classList.remove('ACT');
        });
    };
    
    fontSize.forEach(size => {
        size.addEventListener('click', () => {
        removeSelector();
        let Size;
        size.classList.toggle('ACT');
            if (size.classList.contains('FontSize1')) {
                Size = '10px';
                root.style.setProperty('--sticky-top-left', '5.4rem');
                root.style.setProperty('--sticky-top-top', '5.4rem');
            } else if (size.classList.contains('FontSize2')) {
                Size = '13px';
                root.style.setProperty('--sticky-top-left', '5.4rem');
                root.style.setProperty('--sticky-top-top', '-7rem');
            } else if (size.classList.contains('FontSize3')) {
                Size = '16px';
                root.style.setProperty('--sticky-top-left', '-2rem');
                root.style.setProperty('--sticky-top-top', '-17rem');
            } else if (size.classList.contains('FontSize4')) {
                Size = '19px';
                root.style.setProperty('--sticky-top-left', '-5rem');
                root.style.setProperty('--sticky-top-top', '-25rem');
            } else if (size.classList.contains('FontSize5')) {
                Size = '22px';
                root.style.setProperty('--sticky-top-left', '-12rem');
                root.style.setProperty('--sticky-top-top', '-35rem');
            }
            document.querySelector('html').style.fontSize = Size;
        });
    });
    colorPalette.forEach(color => {
        color.addEventListener('click', () => {
            // Remove 'ACT' class from all colors
            colorPalette.forEach(c => c.classList.remove('ACT'));
    
            let primaryHue;
            if(color.classList.contains('Color1')){
                primaryHue = 252;
            } else if(color.classList.contains('Color2')){
                primaryHue = 52;
            } else if(color.classList.contains('Color3')){
                primaryHue = 352;
            } else if(color.classList.contains('Color4')){
                primaryHue = 152;
            } else if(color.classList.contains('Color5')){
                primaryHue = 202;
            }
            // Add 'ACT' class to the selected color
            color.classList.add('ACT');
    
            root.style.setProperty('--pri-col', primaryHue);
        });
    });
    let lightColor;
    let whiteColor;
    let darkColor;
    const chooseBG = () => {
        root.style.setProperty('--light-col', lightColor);
        root.style.setProperty('--white-col', whiteColor);
        root.style.setProperty('--dark-col', darkColor);
    }
    BG1.addEventListener('click', () => {
        BG1.classList.add('ACT');
        BG2.classList.remove('ACT');
        BG3.classList.remove('ACT');
        window.location.reload();
    });
    BG2.addEventListener('click', () => {
        darkColor = '95%';
        whiteColor = '20%';
        lightColor = '15%';
        BG2.classList.add('ACT');
        BG1.classList.remove('ACT');
        BG3.classList.remove('ACT');
        chooseBG();
    });
    BG3.addEventListener('click', () => {
        darkColor = '95%';
        whiteColor = '10%';
        lightColor = '0%';
        BG2.classList.add('ACT');
        BG1.classList.remove('ACT');
        BG3.classList.remove('ACT');
        chooseBG();
    });
    Settings.addEventListener('click', () => {
        settingModal.style.display = 'grid';
    });

    // Event listener to close settings modal
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('Settings')) {
            settingModal.style.display = 'none';
        }
    });
});
    document.getElementById('editFirstNameButton').addEventListener('click', function() {
        var firstName = document.getElementById('firstName');
        var firstNameInput = document.createElement('input');
        firstNameInput.type = 'text';
        firstNameInput.id = 'firstNameInput';
        firstNameInput.value = firstName.textContent;
        firstName.parentNode.replaceChild(firstNameInput, firstName);
        firstNameInput.focus();
    });
    document.getElementById('editLastNameButton').addEventListener('click', function() {
        var lastName = document.getElementById('lastName');
        var lastNameInput = document.createElement('input');
        lastNameInput.type = 'text';
        lastNameInput.id = 'lastNameInput';
        lastNameInput.value = lastName.textContent;
        lastName.parentNode.replaceChild(lastNameInput, lastName);
        lastNameInput.focus();
    });
    document.getElementById('editEmailButton').addEventListener('click', function() {
        var email = document.getElementById('email');
        var emailInput = document.createElement('input');
        emailInput.type = 'text';
        emailInput.id = 'emailInput';
        emailInput.value = email.textContent;
        email.parentNode.replaceChild(emailInput, email); // Corrected from 'firstName' to 'email'
        emailInput.focus();
    });
    
    document.addEventListener('click', (e) => {
        // Event delegation for save buttons
        if (e.target.id === 'saveFirstChangesButton') {
            saveChanges('firstNameInput', 'new_first_name');
        } else if (e.target.id === 'saveLastChangesButton') {
            saveChanges('lastNameInput', 'new_last_name');
        } else if (e.target.id === 'saveEmailChangesButton') {
            saveChanges('emailInput', 'new_email');
        }
    });
    
    function saveChanges(inputId, fieldName) {
        var inputValue = document.getElementById(inputId).value;
        if (!inputValue) {
            inputValue = document.getElementById(inputId).placeholder;
        }
        // Send AJAX request to update field
        fetch('/update_user_info', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                [fieldName]: inputValue,
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to update ${fieldName}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            // Replace input field with text node
            var parentNode = document.getElementById(inputId).parentNode;
            var newText = document.createTextNode(inputValue);
            parentNode.replaceChild(newText, document.getElementById(inputId));
        })
        .catch((error) => {
            console.error('Error:', error);
        })
        .finally(() => {
            location.reload();
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        // Toggle password visibility
        document.getElementById('togglePasswordVisibility').addEventListener('click', function() {
            var currentPasswordInput = document.getElementById('currentPassword');
            var newPasswordInput = document.getElementById('newPassword');
            
            // Toggle visibility for current password input
            currentPasswordInput.type = (currentPasswordInput.type === 'password') ? 'text' : 'password';
    
            // Toggle visibility for new password input
            newPasswordInput.type = (newPasswordInput.type === 'password') ? 'text' : 'password';
        });
    
        // Change password button click event
        document.getElementById('changePasswordButton').addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default form submission
            
            var currentPassword = document.getElementById('currentPassword').value;
            var newPassword = document.getElementById('newPassword').value;
            
            // Check if the new password is empty
            if (!newPassword.trim()) {
                document.getElementById('errorText').textContent = "New password can't be empty.";
                document.getElementById('errorText').style.display = 'block';
                document.getElementById('successText').style.display = 'none';
                return; // Stop further execution
            }
    
            // Check if the new password is the same as the current password
            if (currentPassword === newPassword) {
                document.getElementById('errorText').textContent = "New password must be different from the current password.";
                document.getElementById('errorText').style.display = 'block';
                document.getElementById('successText').style.display = 'none';
                return; // Stop further execution
            }
            
            // Send a POST request to the server to change the password
            fetch('/change_password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    currentPassword: currentPassword,
                    newPassword: newPassword
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to change password');
                }
                return response.json();
            })
            .then(data => {
                // Password changed successfully
                document.getElementById('errorText').style.display = 'none';
                document.getElementById('successText').style.display = 'block';
                console.log("Password updated successfully: " + newPassword);
            })
            .catch(error => {
                // Error occurred (e.g., incorrect current password)
                document.getElementById('errorText').style.display = 'block';
                document.getElementById('successText').style.display = 'none';
                console.error('Error changing password:', error);
            });
        });
    });
    document.getElementById('deleteAccountButton').addEventListener('click', function() {
        document.getElementById('deleteConfirmation').style.display = 'block';
    });
    
    document.getElementById('cancelDeleteButton').addEventListener('click', function() {
        document.getElementById('deleteConfirmation').style.display = 'none';
    });
    
    document.getElementById('confirmDeleteButton').addEventListener('click', function() {
        var confirmPassword = document.getElementById('confirmPassword').value;
        
        // Check if the confirm password is empty
        if (!confirmPassword.trim()) {
            showAlert('Password can\'t be empty.');
            return;
        }
        
        // Send a POST request to the server to delete the account
        fetch('/delete_account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'confirmPassword=' + encodeURIComponent(confirmPassword)
        })
        .then(response => {
            if (response.status === 400) {
                // Handle incorrect password on the client side
                showAlert('Incorrect password. Please try again.');
                return;
            }
            if (response.status >= 400) {
                throw new Error('Failed to delete account with status code: ' + response.status);
            }
            // Assuming the server redirects to the login page after successful deletion
            window.location.href = response.url;
        })
        .catch(error => {
            // Error occurred (e.g., incorrect password)
            showAlert('Error deleting account: ' + error.message);
        });
    });
    
    function showAlert(message, isError = false) {
        var alertDiv = document.createElement('div');
        alertDiv.className = 'alert';
        if (isError) {
            alertDiv.classList.add('alert-error');
        }
        alertDiv.textContent = message;
        document.body.appendChild(alertDiv);
        
        setTimeout(function() {
            alertDiv.style.display = 'none';
            document.body.removeChild(alertDiv);
        }, 3000); // Hide the alert after 3 seconds
    }
    function showCard() {
        var card = document.getElementById("new-story-card");
        card.style.display = "block";
    }

    // Event listener to show the add story card when the "Add Story" button is clicked
    document.addEventListener('click', (e) => {
        const addStoryButton = document.querySelector('.add-story-button');
        const newStoryCard = document.getElementById("new-story-card");
    
        // Check if the clicked element is the "Add Story" button, the card, or any of their descendants
        const isAddStoryButtonOrCardOrDescendant =
            addStoryButton.contains(e.target) || newStoryCard.contains(e.target);
    
        // If the clicked element is not the "Add Story" button, the card, or any of their descendants, hide the card
        if (!isAddStoryButtonOrCardOrDescendant) {
            newStoryCard.style.display = 'none';
        }
    });
    function showCard() {
        var card = document.getElementById("new-story-card");
        if (card.style.display === "none") {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        var storiesContainer = document.getElementById('storiesContainer');
        var nextButton = document.getElementById('next-button');
        var prevButton = document.getElementById('prev-button');
        var scrollAmount = 0;
    
        nextButton.addEventListener('click', function() {
            // Scroll to the next set of stories
            scrollAmount += storiesContainer.clientWidth; // Adjust this value as needed
            storiesContainer.scrollTo({ left: scrollAmount, behavior: 'smooth' });
        });
    
        prevButton.addEventListener('click', function() {
            // Scroll to the previous set of stories
            scrollAmount -= storiesContainer.clientWidth; // Adjust this value as needed
            storiesContainer.scrollTo({ left: scrollAmount, behavior: 'smooth' });
        });
    });

    // Get the file input element
// Function to handle submission of story form
function submitStoryForm() {
    let storyContent = document.getElementById('story-content').value;
    let imageFile = document.getElementById('file-input').files[0];

    let formData = new FormData();
    formData.append('story_content', storyContent);
    if (imageFile) {
        formData.append('image_file', imageFile);
    }

    for (let [key, value] of formData.entries()) {
        console.log(key, value);
    }

    fetch('/submit_story', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error uploading story:', data.error);
            document.getElementById('form-feedback').textContent = 'Error: ' + data.error;
        } else {
            console.log('Story uploaded successfully', data);
            document.getElementById('form-feedback').textContent = 'Story uploaded successfully!';
            document.getElementById('story-content').value = '';
            document.getElementById('file-input').value = '';
            console.log('Attempting to reload the page...');
            window.location.reload(true);
        }
    })
    .catch(error => {
        console.error('Error uploading story:', error);
        document.getElementById('form-feedback').textContent = 'Error: ' + error.message;
    });
}

