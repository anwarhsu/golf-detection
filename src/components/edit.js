import React from 'react';
import axios from 'axios';

export default function EditButton({ userBox, setuserBox }) {
	const handlePost = (e) => {
		axios
			.post('/edit', {
				userBox,
			})
			.then(function (response) {
				console.log(response);
			})
			.catch(function (error) {
				console.log(error);
			});
	};

	return <button onClick={handlePost}>EDIT</button>;
}
