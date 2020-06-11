function required()
{
var empt = document.forms["inputform"]["term"].value;
if (empt == "")
	{
		alert("All input fields need to be filled before the calculator can be used");
		return false;
	}
else
	{
		return true;
	}

}


