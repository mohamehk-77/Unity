const imgDiv = document.querySelector('.profilePic');
const file = document.querySelector('#File');
const uploadButton = document.querySelector('#uploadButton');
const userId = document.body.getAttribute('data-user-id'); // Assuming you've added a data-user-id attribute to the body tag

imgDiv.addEventListener("mouseenter", function(){
    uploadButton.style.opacity = "1"; // Show upload button
});

imgDiv.addEventListener("mouseleave", function(){
    uploadButton.style.opacity = "0"; // Hide upload button
});

file.addEventListener('change', function(){
    const selectedFile = this.files[0];
    if (selectedFile){
        const reader = new FileReader();
        reader.addEventListener('load', function(){
            imgDiv.style.backgroundImage = `url('${reader.result}')`;
            document.getElementById('pic').src = reader.result; // Update the src of the img tag

            let formData = new FormData();
            formData.append('file', selectedFile);

            fetch('/change_avatar', { // Use the '/change_avatar' endpoint
                method: 'POST',
                body: formData
            }).then(response => {
                if (response.ok) {
                    console.log('Image uploaded successfully');
                    response.json().then(data => {
                        const image_url = data.image_url;
                        document.getElementById('pic').src = image_url; // Update the src with the new image URL
                    });
                } else {
                    console.error('Image upload failed');
                    response.json().then(data => {
                        console.error(data.error); // Log the error message from the server
                    });
                }
            });
        });
        reader.readAsDataURL(selectedFile);
    }
});
