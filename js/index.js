// For the Sign-out menu
const storage = window.localStorage

const showSignOutButton = () => {
    const signout = document.getElementById("sign-out");
    if(storage.clicked === 'false'){
        signout.style.visibility = 'visible';
        storage['clicked'] = 'true';
    } else {
        signout.style.visibility = 'hidden';
        storage['clicked'] = 'false';
    }
}
