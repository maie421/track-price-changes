const container = document.querySelector('#_similar-products');
const loadingLog = document.createElement('p');
loadingLog.textContent = 'Loading...';
container.appendChild(loadingLog);
const urlParams = new URLSearchParams(window.location.search);
const productId = urlParams.get('pid');
const apiUrl = `${window.location.protocol}//${window.location.host}/product/similar?pid=${productId}`;
fetch(apiUrl)
 	.then(res => res.json())
    .then(data => {
		container.removeChild(loadingLog);
        if (data.length > 0){
            data.forEach(product => {
                const productDiv = document.createElement('div');
                productDiv.classList.add('col', 'mb-5');
                productDiv.innerHTML = `
                <a href="/product?pid=${product[0]}">
                    <div class="card h-100">
                        <img class="card-img-top" src="${product[1]}" alt="${product[2]}" />
                        <div class="card-body p-4">
                            <div class="text-center">
                                <h5 class="fw-bolder">${product[2]}</h5>
                                ${product[3]}원
                            </div>
                        </div>
                    </div>
                </a>
                `;
                container.appendChild(productDiv);
            });
        }else{
            loadingLog.textContent = "제품이 없습니다."
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });