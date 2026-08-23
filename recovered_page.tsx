"use client";
import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

type Message = {
  role: string;
  content: string;
  toolActivity?: any[];
  sourcesUsed?: any[];
};

export default function Home() {
  const [activeTab, setActiveTabInternal] = useState('chat');
  const [navHistory, setNavHistory] = useState<string[]>([]);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  
  const setActiveTab = (tab: string) => {
    setSelectedItem(null);
    setNavHistory(prev => [...prev, activeTab]);
    setActiveTabInternal(tab);
  };
  
  const goBack = () => {
    setSelectedItem(null);
    if (navHistory.length > 0) {
      const prev = navHistory[navHistory.length - 1];
      setNavHistory(h => h.slice(0, -1));
      setActiveTabInternal(prev);
    }
  };
  
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setIsDrawerOpen(false);
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, []);

  const goHome = () => {
    setSelectedItem(null);
    setActiveTab('chat');
  };
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [ticketsData, setTicketsData] = useState<any[]>([]);
  const [ordersData, setOrdersData] = useState<any[]>([]);
  const [accountsData, setAccountsData] = useState<any[]>([]);

