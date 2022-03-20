import { Button, IconXCircle, Modal, Space } from "@supabase/ui";
interface ErrorProps {
  title: string;
  children?: React.ReactNode;
  showing: boolean;
  setShowing: (showing: boolean) => void;
}

const Error = ({ title, children, showing, setShowing }: ErrorProps) => {
  return (
    <>
      <Modal
        size="small"
        title={title}
        icon={<IconXCircle background="red" size="xxxlarge" />}
        visible={showing}
        onCancel={() => setShowing(false)}
        // onConfirm={() => setShowing(false)}
        layout="vertical"
        customFooter={[
          <Space key="0" style={{ width: "100%" }}>
            <Button
              danger={true}
              size="medium"
              block
              onClick={() => setShowing(false)}
            >
              Dismiss
            </Button>
          </Space>,
        ]}
      />
    </>
  );
};

export default Error;

// const Error = ({ title, children, setShowing }: ErrorProps) => {
//   return (
//     <div
//       id="error-overlay"
//       className={styles.overlay}
//       onClick={(e) =>
//         (e.target as HTMLElement).id == "error-overlay" && setShowing(false)
//       }
//     >
//       <div className={styles.error}>
//         <Alert title={title} variant="danger" withIcon={true}>
//           {children}
//           <Button onClick={() => setShowing(false)} danger={true}>
//             Dismiss
//           </Button>
//         </Alert>
//       </div>
//     </div>
//   );
// };

// const Error = ({ title, children, showing, setShowing }: ErrorProps) => {
//   return (
//     <Modal
//       title={title}
//       variant="danger"
//       layout="vertical"
//       icon={<IconXCircle size="large" />}
//       visible={showing}
//       customFooter={
//         <Button onClick={() => setShowing(false)} danger={true}>
//           Dismiss
//         </Button>
//       }
//     >
//       {children}
//     </Modal>
//   );
// };
