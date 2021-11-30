import React, { useRef } from 'react';
import axios from 'axios';

export default function DisplayImage({ userBox, setuserBox }) {
	const handleClick = (evt) => {
		var e = evt.target;
		var dim = e.getBoundingClientRect();
		var x = evt.clientX - dim.left;
		var y = evt.clientY - dim.top;
		if (userBox.left_x == '') {
			setuserBox({
				...userBox,
				left_x: x,
				left_y: y,
			});
		} else {
			setuserBox({
				...userBox,
				right_x: x,
				right_y: y,
			});
		}
		alert('x: ' + x + ' y:' + y);
	};
	return (
		<div>
			<div onClick={handleClick}>
				<img src="../htmlfi/golf.jpg" alt="img" width="700" height="700" />
			</div>
			<form enctype="multipart/form-data" action="/upload" method="POST">
				<input id="image-file" type="file" name="file" />
				<br></br>
				<input type="submit" />
			</form>
		</div>
	);
}
