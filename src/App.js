import './App.css';
import React, { useState, useEffect } from 'react';
import DisplayImage from './components/img.js';
import EditButton from './components/edit.js';
import YoloDetect from './components/yolo';
import Distance from './components/distance';

function App() {
	const [initialData, setinitialData] = useState([{}]);
	const [userBox, setuserBox] = useState({
		left_x: '',
		left_y: '',
		right_x: '',
		right_y: '',
	});

	useEffect(() => {
		// fetch('/api')
		// 	.then((response) => response.json())
		// 	.then((data) => setinitialData(data));
		console.log(userBox);
	}, [userBox]);
	return (
		<div className="App">
			<DisplayImage setuserBox={setuserBox} userBox={userBox} />
			<br></br>
			<EditButton setuserBox={setuserBox} userBox={userBox} />
			<br></br>
			<YoloDetect />
			<br></br>
			<Distance />
		</div>
	);
}

export default App;
