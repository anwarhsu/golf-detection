import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function Distance() {
	const handleChange = () => {
		fetch('/distance')
			.then((response) => response.json())
			.then((data) => {
				console.log(data);
			});
	};

	return (
		<div>
			<button onClick={handleChange}>distance calc</button>
			<br></br>
			<img src="../htmlfi/golf_YOLO_distance.jpg" width="1000" height="1000" />
		</div>
	);
}
