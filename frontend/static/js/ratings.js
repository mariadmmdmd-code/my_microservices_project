class RatingsSystem {
    constructor(pageName) {
        this.pageName = pageName;
        this.pollingInterval = null;
        this.init();
    }
    
    async init() {
        await this.updateRatingsDisplay();
        this.attachEventListeners();
        this.startPolling();
    }
    
    async updateRatingsDisplay() {
        try {
            const response = await fetch(`/api/get-ratings?page_name=${this.pageName}`);
            const data = await response.json();
            
            const likesSpan = document.getElementById('likes-count');
            const dislikesSpan = document.getElementById('dislikes-count');
            
            if (likesSpan) likesSpan.textContent = data.likes;
            if (dislikesSpan) dislikesSpan.textContent = data.dislikes;
        } catch (error) {
            console.error('Error fetching ratings:', error);
        }
    }
    
    attachEventListeners() {
        const likeBtn = document.getElementById('like-btn');
        const dislikeBtn = document.getElementById('dislike-btn');
        const resetBtn = document.getElementById('reset-btn');

        console.log('Buttons found:', { likeBtn: !!likeBtn, dislikeBtn: !!dislikeBtn, resetBtn: !!resetBtn });
        
        if (likeBtn) {
            const newLikeBtn = likeBtn.cloneNode(true);
            likeBtn.parentNode.replaceChild(newLikeBtn, likeBtn);
            newLikeBtn.addEventListener('click', () => this.sendRating('like'));
        }
        
        if (dislikeBtn) {
            const newDislikeBtn = dislikeBtn.cloneNode(true);
            dislikeBtn.parentNode.replaceChild(newDislikeBtn, dislikeBtn);
            newDislikeBtn.addEventListener('click', () => this.sendRating('dislike'));
        }
        
        if (resetBtn) {
            const newResetBtn = resetBtn.cloneNode(true);
            resetBtn.parentNode.replaceChild(newResetBtn, resetBtn);
            newResetBtn.addEventListener('click', () => this.resetRatings());
        }
    }
    
    async sendRating(type) {
        try {
            const response = await fetch('/api/rate', {  
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    page_name: this.pageName,
                    type: type
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                document.getElementById('likes-count').textContent = data.likes;
                document.getElementById('dislikes-count').textContent = data.dislikes;
            }
        } catch (error) {
            console.error('Error sending rating:', error);
        }
    }
    
    async resetRatings() {
        console.log('resetRatings called for page:', this.pageName);
        
        try {
            const response = await fetch('/api/reset-ratings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    page_name: this.pageName
                })
            });
            
            console.log('Reset response status:', response.status);
            const data = await response.json();
            console.log('Reset response data:', data);
            
            if (data.success) {
                document.getElementById('likes-count').textContent = 0;
                document.getElementById('dislikes-count').textContent = 0;
            } else {
                console.error('Reset failed:', data.error);
            }
        } catch (error) {
            console.error('Error resetting ratings:', error);
        }
    }
    
    getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }
    
    startPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
        }
        
        this.pollingInterval = setInterval(() => {
            this.updateRatingsDisplay();
        }, 1000);
    }
    
    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
    }
}

// запуск рейтинга
document.addEventListener('DOMContentLoaded', () => {
    const pageContainer = document.querySelector('[data-page-name]');
    if (pageContainer && !window.ratingsSystem) {
        const pageName = pageContainer.dataset.pageName;
        window.ratingsSystem = new RatingsSystem(pageName);
    }
});