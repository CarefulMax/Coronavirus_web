const regionInput = document.getElementById("regionsInput")
const startDateInput = document.getElementById("startDateInput")
const endDateInput = document.getElementById("regionsInput")
console.log('Е бой')


function datesCheck(){
	startDate = startDateInput.value;
	endDate = endDateInput.value;
	console.log(startDate);
	console.log(endDate);
	if (startDate=='' || endDate==''){
		console.log('Есть пустые')
	}
}

startDateInput.addEventListener('change', datesCheck);
endDateInput.addEventListener('change', datesCheck);