import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function YoloDetect() {
	const [state, setState] = useState(false);

	useEffect(() => {
		// fetch('/api')
		// 	.then((response) => response.json())
		// 	.then((data) => setinitialData(data));
		console.log(state);
	}, [state]);
	const handleChange = () => {
		fetch('/yolo')
			.then((response) => response.json())
			.then((data) => {
				console.log(data);
				setState(true);
			});
	};

	return (
		<div>
			<button onClick={handleChange}>YOLO DETECT</button>
			<br></br>
			<img src="../htmlfi/golf_YOLO.jpg" width="1000" height="1000" />
		</div>
	);
}
