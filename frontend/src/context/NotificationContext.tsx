import React, { createContext, useState, useContext, ReactNode } from 'react';
import Notification, { NotificationType } from '../components/common/Notification';

interface NotificationContextProps {
  showNotification: (type: NotificationType, message: string, title?: string) => void;
  hideNotification: () => void;
}

const NotificationContext = createContext<NotificationContextProps | undefined>(undefined);

interface NotificationProviderProps {
  children: ReactNode;
}

export const NotificationProvider: React.FC<NotificationProviderProps> = ({ children }) => {
  const [open, setOpen] = useState(false);
  const [type, setType] = useState<NotificationType>('info');
  const [message, setMessage] = useState('');
  const [title, setTitle] = useState<string | undefined>(undefined);

  const showNotification = (
    notificationType: NotificationType,
    notificationMessage: string,
    notificationTitle?: string
  ) => {
    setType(notificationType);
    setMessage(notificationMessage);
    setTitle(notificationTitle);
    setOpen(true);
  };

  const hideNotification = () => {
    setOpen(false);
  };

  return (
    <NotificationContext.Provider value={{ showNotification, hideNotification }}>
      {children}
      <Notification
        open={open}
        type={type}
        message={message}
        title={title}
        onClose={hideNotification}
      />
    </NotificationContext.Provider>
  );
};

export const useNotification = (): NotificationContextProps => {
  const context = useContext(NotificationContext);
  if (context === undefined) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return context;
};
