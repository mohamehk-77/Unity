document.addEventListener("DOMContentLoaded", function() {
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
});