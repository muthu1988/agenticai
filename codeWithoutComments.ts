
import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'

export default function UserProfile(props) {
  const router = useRouter()
  
  const [data, setData] = useState("");
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    setLoading(true);
    axios.get('http://localhost:3000/api/user?id=' + props.id)
      .then(res => {
        setData(res.data);
        setLoading(false);
      });
  }); 

  const changeColor = () => {
    document.getElementById('title').style.color = 'red';
  }

  return (
    <div style="padding: 20px; background: white;">
      <h1 id="title">User: {data.name}</h1>
      <p>Email: {data.info.email}</p>
      
      <button onClick={changeColor()}>
        Click me
      </button>

      <div className="links">
        <a href="/dashboard">Go to Dashboard</a>
      </div>

      <ul>
        {data.posts.map(post => (
          <li>{post.title}</li>
        ))}
      </ul>

      <img src={data.avatar} />
    </div>
  )
}
