document.addEventListener('DOMContentLoaded', function () {
    const exchangeRatesScript = document.getElementById('exchangeRatesJson');
    const exchangeRates = exchangeRatesScript ? JSON.parse(exchangeRatesScript.textContent) : {};

    const fromCurrencySelect = document.getElementById('fromCurrency');
    const toCurrencySelect = document.getElementById('toCurrency');
    const amountInput = document.getElementById('amount');
    const convertBtn = document.getElementById('convertBtn');
    const conversionResult = document.getElementById('conversionResult');
    const tbody = document.querySelector('#exchangeRatesTable tbody');

    function populateCurrencySelects() {
        const currencyCodes = Object.keys(exchangeRates).sort();

        currencyCodes.forEach(code => {
            const option1 = document.createElement('option');
            option1.value = code;
            option1.textContent = code;
            fromCurrencySelect.appendChild(option1);

            const option2 = document.createElement('option');
            option2.value = code;
            option2.textContent = code;
            toCurrencySelect.appendChild(option2);
        });

        if (exchangeRates['USD']) fromCurrencySelect.value = 'USD';
        if (exchangeRates['EUR']) toCurrencySelect.value = 'EUR';
    }

    function updateExchangeRatesTable() {
        tbody.innerHTML = '';
        const sortedRates = Object.entries(exchangeRates).sort();

        sortedRates.forEach(([currency, rate]) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${currency}</td>
                <td>${rate.toFixed(4)}</td>
            `;
            tbody.appendChild(row);
        });
    }

    function convertCurrency() {
        const amount = parseFloat(amountInput.value);
        const from = fromCurrencySelect.value;
        const to = toCurrencySelect.value;

        if (isNaN(amount) || amount <= 0) {
            conversionResult.textContent = 'Veuillez entrer un montant valide.';
            return;
        }

        if (!exchangeRates[from] || !exchangeRates[to]) {
            conversionResult.textContent = 'Devise non prise en charge.';
            return;
        }

        const rate = exchangeRates[to] / exchangeRates[from];
        const result = amount * rate;

        conversionResult.textContent = `Résultat : ${result.toFixed(4)} ${to}`;
    }
    convertBtn.addEventListener('click', convertCurrency);
    populateCurrencySelects();
    updateExchangeRatesTable();
});
