function showFlash(message, type) {
      const overlay = document.getElementById('overlay');
      const box = document.getElementById('messageBox');
      const text = document.getElementById('messageText');

      text.textContent = message;
      box.className = 'message-box ' + type;

      overlay.style.display = 'flex';

      // Auto hide after 10 seconds
      setTimeout(hideFlash, 10000);
    }

    function hideFlash() {
      document.getElementById('overlay').style.display = 'none';
    }

    // On page load, check for flash messages and show overlay
    window.onload = function() {
      const flashMessages = document.querySelectorAll('#flash-messages .flash-message');
      if (flashMessages.length > 0) {
        const firstMsg = flashMessages[0];
        const message = firstMsg.textContent.trim();
        const classes = firstMsg.className.split(' ');

        let type = 'success';  

        if (classes.includes('error')) {
          type = 'error';
        } else if (classes.includes('success')) {
          type = 'success';
        }

        showFlash(message, type);
      }
    }